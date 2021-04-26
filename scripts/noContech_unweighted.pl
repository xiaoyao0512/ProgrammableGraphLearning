#!/usr/bin/perl -w
use strict;
no warnings 'experimental::smartmatch';

my $ARGC = scalar @ARGV;
if ($ARGC < 1) {
	print "\nusage: perl exe.pl <a file you want to instrument>\n\n";
	exit 1;
}

my $file = $ARGV[0];
my @arguments = @ARGV[1..$ARGC - 1];
print "arguments: @arguments\n";
my %BBs;
my $index = -1;
my $BB = 0;
my @global;
my @str;
###################Instrument the file##############################
my $numOfStr = 0;
my $isStr = 0;
my $isPrinted = 0;
my $numOfBB = 0;
my $doNotPrint = 0;
my $numOfSL = 0;
my $main = 0;
my $hasPrint = 0;
my %func;
my %callFunc;
my $printf = 0;
my $SL = 0;
my %BasicBlocks;
my $BBbegin = 0;
my @space;
my @timing;
my @printf;

system("clang -emit-llvm -S -c $file -o llvm.ll");

open(IN, "llvm.ll");
open(OUT, ">llvm_instrumented.ll");

while (<IN>) {
	chomp;
	$BBbegin = 0 if (/(clang version)|br|ret/);
	if ($BBbegin) {
		push @{$BasicBlocks{$numOfBB}}, $_;
	}
	if (/global/) {
		push @global, $_;
		#print;
		#next;
	}
	if (/private unnamed_addr/) {
		push @str, $_;
	}
	if (/^@.str/) {
		$numOfStr++;
		$isStr = 1;
	}
	$hasPrint = 1 if (/printf/);
	if (/^(?!@)/gm && $isStr) {
		$isStr = 0;
		$SL = $numOfStr;
		print OUT "\@.str." . "$numOfStr" ." = private unnamed_addr constant [17 x i8] c\"counter is %lli\\0A\\00\", align 1\n";
		$isPrinted = 1;
		$numOfStr++;
		$printf = $numOfStr;
		print OUT "\@.str." . "$numOfStr" ." = private unnamed_addr constant [18 x i8] c\"BasicBlock# = %d\\0A\\00\", align 1\n";
	}
	if (/; Function Attrs:/ && !$isPrinted && !$doNotPrint) {
		print OUT "\@.str.$numOfStr = private unnamed_addr constant [17 x i8] c\"counter is %lli\\0A\\00\", align 1\n\n";
		$doNotPrint = 1;
	}
	if (/store|load/) { #before load/store instr, instrument rdsc()
		$numOfSL++;
		print OUT "  %SL" . "$numOfSL" . " = call i64 \@rdtsc()\n";
	}
	print OUT;
	print OUT "\n";
	if (/define (.*) \@(.*)\((.*)\)/) {
		#print "$2\n";
		my $fncName = $1;
		$BBbegin = 1;
		my @args = split /,/, $2;
		#print "args: $#args\n";
		#print "@args\n";
		#push @{$func{$1}}, ($#args + 1);
		push @{$func{$fncName}}, @args;

		#foreach my $pair (@args) {
		#	my @temp = split/ /, $pair;
		#	foreach my $item (@temp) {
		#		#print "temp: $item\n";
		#		if ($item =~ /^%/) {
		#			#print "$item\n";
		#			push @{$func{$fncName}}, $item;
		#		}
		#	}
		#}
		$numOfBB++;
		print OUT "%print$numOfBB = call i32 (i8*, ...) \@printf(i8* getelementptr inbounds ([18 x i8], [18 x i8]* @.str.$printf, i32 0, i32 0), i32 $numOfBB);\n";
	}
	if (/call .* \@(.*)\((.*)\)/) {
		#print "$2\n";
		my $fncName = $1;
		my @args = split /,/, $2;
		#print "args: $#args\n";
		#print "$fncName: @args\n";
		#push @{$func{$1}}, ($#args + 1);
		push @{$callFunc{$fncName}}, @args;
		#foreach my $pair (@args) {
		#	my @temp = split/ /, $pair;
		#	foreach my $item (@temp) {
		#		#print "temp: $item\n";
		#		if ($item =~ /^%/) {
		#			#print "$item\n";
		#			push @{$callFunc{$fncName}}, $item;
		#		}
		#	}
		#}
		$numOfBB++;
		$BBbegin = 1;
		print OUT "%print$numOfBB = call i32 (i8*, ...) \@printf(i8* getelementptr inbounds ([18 x i8], [18 x i8]* @.str.$printf, i32 0, i32 0), i32 $numOfBB);\n";
	}
	if (/; <label>:/) {
		$numOfBB++;
		$BBbegin = 1;
		print OUT "%print$numOfBB = call i32 (i8*, ...) \@printf(i8* getelementptr inbounds ([18 x i8], [18 x i8]* @.str.$printf, i32 0, i32 0), i32 $numOfBB);\n";
	}
	if (/(store|load) .*, align (\d+)/) {
		push @space, $2;

		$numOfSL++;
		print OUT "  %SL" . "$numOfSL" . " = call i64 \@rdtsc()\n";
		$numOfSL++;
		my $temp1 = $numOfSL - 1;
		my $temp2 = $numOfSL - 2;
		print OUT "  %SL" . "$numOfSL" . " = sub i64 %SL$temp1, %SL$temp2\n";
		$numOfSL++;
		$temp1 = $numOfSL - 1;
		print OUT "  %SL$numOfSL = call i32 (i8*, ...) \@printf(i8* getelementptr inbounds ([17 x i8], [17 x i8]* \@.str.$SL, i32 0, i32 0), i64 %SL$temp1)\n";	
	}

	if (/define (.*) \@main\(.*\) \#\d+/) {
		$main = 1;
	}
	if (/^}/ && $main) {
		$main = 0;
		print OUT "\n\n; Function Attrs: nounwind uwtable\n";
		print OUT "define i64 \@rdtsc() #0 {\n";
		print OUT "  %lo = alloca i32, align 4\n";
		print OUT "  %hi = alloca i32, align 4\n";
		print OUT "  %1 = call { i32, i32 } asm sideeffect \"rdtsc\", \"={ax},={dx},~{dirflag},~{fpsr},~{flags}\"() #2, !srcloc !1\n";
		print OUT "  %2 = extractvalue { i32, i32 } %1, 0\n";
		print OUT "  %3 = extractvalue { i32, i32 } %1, 1\n";
		print OUT "  store i32 %2, i32* %lo, align 4\n";
		print OUT "  store i32 %3, i32* %hi, align 4\n";
		print OUT "  %4 = load i32, i32* %hi, align 4\n";
		print OUT "  %5 = zext i32 %4 to i64\n";
		print OUT "  %6 = shl i64 %5, 32\n";
		print OUT "  %7 = load i32, i32* %lo, align 4\n";
		print OUT "  %8 = zext i32 %7 to i64\n";
		print OUT "  %9 = or i64 %6, %8\n";
		print OUT "  ret i64 %9\n";
		print OUT "}\n";
		print OUT "\n!1 = !{i32 330}\n";
		print OUT "\ndeclare i32 \@printf(i8*, ...) #0\n\n" if !$hasPrint;
	}

}

close(IN);
close(OUT);
system("lli llvm_instrumented.ll @arguments > timing");
#if (defined $ARGV[1]) {
#	system("lli llvm_instrumented.ll $ARGV[1] > timing");
# else {
#	system("lli llvm_instrumented.ll > timing");
#}
open(OUT, ">$file.ll");
open(IN, "timing");

my $currentBB = 0;
while(<IN>) {
	chomp;
	if (/counter is (\d+)/) {
		push @timing, $1;
	} elsif (/BasicBlock# = (\d+)/) {
		$currentBB = $1;
		if (defined $BasicBlocks{$currentBB}) {
			foreach my $instruction (@{$BasicBlocks{$currentBB}}) {
				print OUT "$instruction\n";
			}
		}
	}
}

close(OUT);
close(IN);



my %des;
my %src;

open(IN, "$file.ll");
#open(IN, "test.ll");
#open(IN, "temp.ll");
print "Starting...\n";
my $node = 0;
my %dep1;
#print "@\n";

#print "skipStore: @skipStore\n";
while(<IN>) {
	chomp;
	if (/\s*(.*) = call (.*) \@printf\((.*) \w+ \w+ (.*)\* (.*), i\d+ \d+, i\d+/) {
#		print;
#		print "16\n$1\t$5\n";
		my $dest = $1;
		my $source = $5;
		$dep1{$node}[0] = $node - 1;
		foreach my $i (keys %des) {
			if ($source eq $i) {
				$dep1{$node}[1] = $des{$source};
				last;
			}
		}
		$src{$source} = $node;
		$des{$dest} = $node;
	} elsif (/\s*(.*) = \w+ i\d+ \@\w+\(i\d+(\*)? (.*), i\d+(\*)? (.*)\)/) {
#		print;
#		print "10\n";
		my $dest = $1;
		my $source = $3;
		my $source2 = $5;
		$dep1{$node}[0] = $node - 1;
		foreach my $i (keys %des) {
			if ($source eq $i) {
				if (!defined $dep1{$node}) {
					${$dep1{$node}}[1] = $des{$source};
				} else {
					${$dep1{$node}}[2] = $des{$source};
				}
				$src{$source} = $node;
				$source = "XXXX";
			} 
			if ($source2 eq $i) {
				if (!defined $dep1{$node}) {
					${$dep1{$node}}[1] = $des{$source2};
				} else {
					${$dep1{$node}}[2] = $des{$source2}; 
				}
				$src{$source2} = $node;
				$source2 = "XXXX";
			}
		}
		$des{$dest} = $node;
	} elsif (/\s*(.*) = call.*\@(fopen|.*fscanf|.*alloc)\(.*\* (.*), i\d+\* \w+?/) {
#		print;
#		print "13\n";
		my $dest = $1;
		my $source = $3;
#		print "dest: $1\tsrc: $3\n";
		$dep1{$node}[0] = $node - 1;
		foreach my $i (keys %des) {
			if ($source eq $i) {
				$dep1{$node}[1] = $des{$source};
				last;
			}
		}
		$src{$source} = $node;
		$des{$dest} = $node;
	} elsif (/\s*(.*) = call .*\@.*\(\w+ (.*), \w+ (.*), \w+ .*, \w+ .*, \w+ .*, i\d+ .*,.*/) {
#		print;
#		print "17\n";
#		print "src: $2\t$3\n";
		my $dest = $1;
		my $source = $2;
		my $source2 = $3;
		$dep1{$node}[0] = $node - 1;
		foreach my $i (keys %des) {
			if ($source eq $i) {
				if (!defined $dep1{$node}) {
					${$dep1{$node}}[1] = $des{$source};
				} else {
					${$dep1{$node}}[2] = $des{$source};
				}
				$src{$source} = $node;
				$source = "XXXX";
			} 
			if ($source2 eq $i) {
				if (!defined $dep1{$node}) {
					${$dep1{$node}}[1] = $des{$source2};
				} else {
					${$dep1{$node}}[2] = $des{$source2}; 
				}
				$src{$source2} = $node;
				$source2 = "XXXX";
			}
		}
		$des{$dest} = $node;
	} elsif (/\s+(.*) = call \w+ i\d+\*? \@.*\(i\d+ (.*), i\d+ (.*)\)/) {
#		print;
#		print "17\n";
#		print "$2\t$3\n";
		my $dest = $1;
		my $source = $2;
		my $source2 = $3;
		$dep1{$node}[0] = $node - 1;
		foreach my $i (keys %des) {
			if ($source eq $i) {
				if (!defined $dep1{$node}) {
					${$dep1{$node}}[1] = $des{$source};
				} else {
					${$dep1{$node}}[2] = $des{$source};
				}
				$src{$source} = $node;
				$source = "XXXX";
			} 
			if ($source2 eq $i) {
				if (!defined $dep1{$node}) {
					${$dep1{$node}}[1] = $des{$source2};
				} else {
					${$dep1{$node}}[2] = $des{$source2}; 
				}
				$src{$source2} = $node;
				$source2 = "XXXX";
			}
		}
		$des{$dest} = $node;
	} elsif (/\s*(.*) = call [\s\S]*\@\w+\((.*,)?\s*.*\*? (.*)\)/) {
#		print;
#		print "8\n";
		my $dest = $1;
		my $source = $3;
		$dep1{$node}[0] = $node - 1;
#		print "dest: $1\tsrc: $3\n";
		foreach my $i (keys %des) {
			if ($source eq $i) {
				$dep1{$node}[1] = $des{$source};
				last;
			}
		}
		$src{$source} = $node;
		$des{$dest} = $node;
	} elsif (/\s*(.*) = alloca/) {
		$des{$1} = $node;
	} elsif (/\s*(.*) = private unnamed_addr/) {
		$des{$1} = $node;
	} elsif (/store\s+(.*)\s+(.*),\s+(.*)\s+(.*), align/) {
#		print;
		#print "\n";
#		print "1\n";
		#print "$2\n";
		my $dest = $4;
		my $size; my $time; my $latency;
		#print "dest node : $dest\n";
		my $source = $2;
		my $inst = $_;
			$size = 4;
			$time = pop @timing;
			$latency = $time * ($size);

		if ($source =~ /^\d+$/) {
			foreach my $i (keys %des) {
				#print "loop: $i\n";
				if ($dest eq $i) {
					${$dep1{$node}}[0] = "store";
					${$dep1{$node}}[1] = $des{$dest};
					#print "$des{$dest}\n";
					${$dep1{$node}}[2] = 1;
					last;
				}
			}
		} else {
			my $firstWord = 0;
			foreach my $i (keys %des) {
				if ($source eq $i) {
					if (!$firstWord) {
						push @{$dep1{$node}}, "store";
						$firstWord = 1;
					}
					push @{$dep1{$node}}, $des{$source};
					push @{$dep1{$node}}, 1;
					#${$dep1{$node}}[0] = "store";
					#${$dep1{$node}}[1] = $des{$source};
					#print "$des{$dest}\n";
					#${$dep1{$node}}[2] = $latency;
				}
				if ($dest eq $i) {
					if (!$firstWord) {
						push @{$dep1{$node}}, "store";
						$firstWord = 1;
					}
					push @{$dep1{$node}}, $des{$dest};
					push @{$dep1{$node}}, 1;
					#${$dep1{$node}}[3] = $des{$dest};
					#print "$des{$dest}\n";
					#${$dep1{$node}}[4] = $latency;
				}

			}
			$src{$source} = $node;
		}
		#print "store latency = $latency\n";
		#print "dep = $des{$dest}\n";
		$des{$dest} = $node;
		#print "$dest = $node\n";
	} elsif (/\s*(.*) = (load) (.*), (.*) (.*), align/) { # load
#		print;
#		print "\n";
#		print "2\n";
		#print "$1\t$5\n";
		my $dest = $1;
		my $source = $5;
		#print "src : $5\n";
		my $size = 4;
		my $time = pop @timing;
		my $latency = $time * ($size);
		foreach my $i (keys %des) {
			#print "$i\n";
			if ($source eq $i) {
				${$dep1{$node}}[0] = "latency";
				${$dep1{$node}}[1] = $des{$source};
				#print "$des{$source}\n";
				${$dep1{$node}}[2] = 1;
				#print "load latency = $latency\n";
				last;
			}
		}
		$src{$source} = $node;
		$des{$dest} = $node;
	} elsif (/\s*(.*) = (\w+) (\w+) i(\d+) (.*), (.*)\s*/) { # add
#		print;
#		print "3\n";
		my $dest = $1;
		my $source = $5;
		my $source2 = $6;
		foreach my $i (keys %des) {
			if ($source eq $i) {
				if (!defined $dep1{$node}) {
					${$dep1{$node}}[0] = $des{$source};
				} else {
					${$dep1{$node}}[1] = $des{$source};
				}
				$src{$source} = $node;
				$source = "XXXX";
				#last;
			} 
			if ($source2 eq $i) {
				if (!defined $dep1{$node}) {
					${$dep1{$node}}[0] = $des{$source2};
				} else {
					${$dep1{$node}}[1] = $des{$source2}; 
				}
				$src{$source2} = $node;
				$source2 = "XXXX";
				#last;;
			}
		}
		#$src{$source} = $node;
		#$src{$source2} = $node;
		$des{$dest} = $node;
	} elsif (/\s*(.*) = \w+ (.*) (.*) to (.*)/) { # sext
#		print;
#		print "4\n";
		my $dest = $1;
		my $source = $3;
		#print $5;
		foreach my $i (keys %des) {
			if ($source eq $i) {
				$dep1{$node} = $des{$source};
				last;
			}
		}
		$src{$source} = $node;
		$des{$dest} = $node;
	} elsif (/\s*(.*) = \w+ \w+ \[.*\], \[.*\]\* (.*), i\d+ \d+, i\d+ (.*)\s*/) {
#		print;
#		print "5\n";
		my $dest = $1;
		my $source = $2;
		my $source2 = $3;
		foreach my $i (keys %des) {
			if ($source eq $i) {
				if (!defined $dep1{$node}) {
					${$dep1{$node}}[0] = $des{$source};
				} else {
					${$dep1{$node}}[1] = $des{$source};
				}
				$src{$source} = $node;
				$source = "XXXX";
			} 
			if ($source2 eq $i) {
				if (!defined $dep1{$node}) {
					${$dep1{$node}}[0] = $des{$source2};
				} else {
					${$dep1{$node}}[1] = $des{$source2}; 
				}
				$src{$source2} = $node;
				$source2 = "XXXX";
			}
		}
		$des{$dest} = $node;
	} elsif (/(.*) = common global/) {
		#print;
		$des{$1} = $node;
	} elsif (/\s*(.*) = getelementptr inbounds (.*), (.*) (.*), (.*) (.*), (.*) (.*)/) { 
#		print;
#		print "7\n";
		my $dest = $1;
		my $source = $4;
		my $source2 = $6;
#		print "source1: $4, source2: $6\n";
		foreach my $i (keys %des) {
			if ($source eq $i) {
				if (!defined $dep1{$node}) {
					${$dep1{$node}}[0] = $des{$source};
				} else {
					${$dep1{$node}}[1] = $des{$source};
				}
				$src{$source} = $node;
				$source = "XXXX";
			} 
			if ($source2 eq $i) {
				if (!defined $dep1{$node}) {
					${$dep1{$node}}[0] = $des{$source2};
				} else {
					${$dep1{$node}}[1] = $des{$source2}; 
				}
				$src{$source2} = $node;
				$source2 = "XXXX";
			}
		}
		$des{$dest} = $node;
	} elsif (/\s*(.*) = \w+ i\d+ (.*), i\d+ (.*), i\d+/) {
#		print;
#		print "14\n";
#		print "$1\t$2\t$3\n";
		my $dest = $1;
		my $source = $2;
		my $source2 = $3;
		foreach my $i (keys %des) {
			if ($source eq $i) {
				if (!defined $dep1{$node}) {
					${$dep1{$node}}[0] = $des{$source};
				} else {
					${$dep1{$node}}[1] = $des{$source};
				}
				$src{$source} = $node;
				$source = "XXXX";
			} 
			if ($source2 eq $i && $source2 =~ /^%/) {
				if (!defined $dep1{$node}) {
					${$dep1{$node}}[0] = $des{$source2};
				} else {
					${$dep1{$node}}[1] = $des{$source2}; 
				}
				$src{$source2} = $node;
				$source2 = "XXXX";
			}
		}
		$des{$dest} = $node;
	} elsif (/\s*(.*) = \w+ \w+ (.*) (.*), (.*)? (.*)/) {
#		print;
#		print "11\n";
		#print "$1\t$3\t$5\n";
		my $dest = $1;
		my $source = $3;
		my $source2 = $5;
		foreach my $i (keys %des) {
			if ($source eq $i) {
				if (!defined $dep1{$node}) {
					${$dep1{$node}}[0] = $des{$source};
				} else {
					${$dep1{$node}}[1] = $des{$source};
				}
				$src{$source} = $node;
				$source = "XXXX";
			} 
			if ($source2 eq $i && $source2 =~ /^%/) {
				if (!defined $dep1{$node}) {
					${$dep1{$node}}[0] = $des{$source2};
				} else {
					${$dep1{$node}}[1] = $des{$source2}; 
				}
				$src{$source2} = $node;
				$source2 = "XXXX";
			}
		}
		$des{$dest} = $node;
	 
	} elsif (/\s*(.*) = \w+ \w+ (.*) (.*), (.*)/) {
#		print;
#		print "12\n";
#		print "$1\t$3\t$4\n";
		my $dest = $1;
		my $source = $3;
		my $source2 = $4;
		foreach my $i (keys %des) {
			if ($source eq $i) {
				if (!defined $dep1{$node}) {
					${$dep1{$node}}[0] = $des{$source};
				} else {
					${$dep1{$node}}[1] = $des{$source};
				}
				$src{$source} = $node;
				$source = "XXXX";
			} 
			if ($source2 eq $i) {
				if (!defined $dep1{$node}) {
					${$dep1{$node}}[0] = $des{$source2};
				} else {
					${$dep1{$node}}[1] = $des{$source2}; 
				}
				$src{$source2} = $node;
				$source2 = "XXXX";
			}
		}
		$des{$dest} = $node;
	} elsif (/\s*(.*) = \w+ \w+ (.*), (.*)/) {
#		print;
#		print "6\n";
#		print "$1\t$2\t$3\n";
		my $dest = $1;
		my $source = $2;
		my $source2 = $3;
		foreach my $i (keys %des) {
			if ($source eq $i) {
				if (!defined $dep1{$node}) {
					${$dep1{$node}}[0] = $des{$source};
				} else {
					${$dep1{$node}}[1] = $des{$source};
				}
				$src{$source} = $node;
				$source = "XXXX";
			} 
			if ($source2 eq $i) {
				if (!defined $dep1{$node}) {
					${$dep1{$node}}[0] = $des{$source2};
				} else {
					${$dep1{$node}}[1] = $des{$source2}; 
				}
				$src{$source2} = $node;
				$source2 = "XXXX";
			}
		}
		$des{$dest} = $node;
	} elsif (/call .* \@.*\(.* (.*)\)/) {
#		print;
#		print "15\n";
#		print "$1\n";
		my $source = $1;
		my $source2 = $node - 1;
		if (!defined $dep1{$node}) {
			${$dep1{$node}}[0] = $source2;
		} else {
			${$dep1{$node}}[1] = $source2; 
		}
		foreach my $i (keys %des) {
			if ($source eq $i) {
				if (!defined $dep1{$node}) {
					${$dep1{$node}}[0] = $des{$source};
				} else {
					${$dep1{$node}}[1] = $des{$source} if ($des{$source} != ${$dep1{$node}}[0]);
				}
				$src{$source} = $node;
				#$source = "XXXX";
				last;
			}
		}
	} 
	$node++;
}
#foreach my $index (keys %dep1) {
#	if (ref($dep1{$index}) eq 'ARRAY') {
#		print "$index -> ${$dep1{$index}}[0]\n";
#		print "$index -> ${$dep1{$index}}[1]\n" if defined ${$dep1{$index}}[1];
#		next;
#	}
#	print "$index -> $dep1{$index}\n";
#}
close(IN);
#=cut
my @arr1; my @arr2;
foreach my $index (keys %dep1) {
	if (ref($dep1{$index}) eq 'ARRAY') {
		if (${$dep1{$index}}[0] ne "latency" && ${$dep1{$index}}[0] ne "store") {
			push @arr1, [$index, ${$dep1{$index}}[0], 1];
			push @arr2, [${$dep1{$index}}[0], $index, 1];
			if (defined ${$dep1{$index}}[1]) {
				push @arr1, [$index, ${$dep1{$index}}[1], 1];
				push @arr2, [${$dep1{$index}}[1], $index, 1];	
				if (defined ${$dep1{$index}}[2]) {
					push @arr1, [$index, ${$dep1{$index}}[2], 1];
					push @arr2, [${$dep1{$index}}[2], $index, 1];	
				}
			}
			
		} elsif (${$dep1{$index}}[0] eq "latency") {
			push @arr1, [$index, ${$dep1{$index}}[1], 1];
			push @arr2, [${$dep1{$index}}[1], $index, 1];
		} elsif (${$dep1{$index}}[0] eq "store") {
			push @arr1, [$index, ${$dep1{$index}}[1], 1];
			push @arr2, [${$dep1{$index}}[1], $index, 1];
			if (defined ${$dep1{$index}}[3]) {
				push @arr1, [$index, ${$dep1{$index}}[3], 1];
				push @arr2, [${$dep1{$index}}[3], $index, 1];
			}
		}
		next;
	}
	push @arr1, [$index, $dep1{$index}, 1];
	push @arr2, [$dep1{$index}, $index, 1];
}

#foreach my $i (@arr1) {
#	foreach my $j (@{$i}) {
#		print "arr1: $j\n";
#	}
#	print "*************\n";
#}

my @sortedArr1 = sort {$a->[0] <=> $b->[0] || $a->[1] <=> $b->[1]} @arr1;
my @sortedArr2 = sort {$a->[0] <=> $b->[0] || $a->[1] <=> $b->[1]} @arr2;
my $numOfEdges = $#sortedArr1 + 1;
#print "#edge $numOfEdges\n";
my $numOfNodes = ${$sortedArr1[$numOfEdges - 1]}[0];
open(OUT2, ">$file.gexf");
# some header information
print OUT2 "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n";
print OUT2 "<gexf xmlns:viz=\"http://www.gexf.net/1.1draft/viz\" ",
"version=\"1.1\" xmlns=\"http://www.gexf.net/1.1draft\">\n";
print OUT2 "<meta lastmodifieddate=\"2017-03-01+6:30\">\n";
print OUT2 "<creator>Gephi 0.7</creator>\n";
print OUT2 "</meta>\n";
print OUT2 "<graph defaultedgetype=\"directed\" idtype=\"string\" ",
"type=\"static\">\n";
my $nodes = $numOfNodes + 1;
print OUT2 "<nodes count=\"$nodes\">\n";
foreach my $idx (0..($numOfNodes)) {
	print OUT2 "<node id=\"$idx.0\" label=\"node#$idx\"/>\n";
}
print OUT2 "</nodes>\n";
print OUT2 "<edges count=\"$numOfEdges\">\n";
foreach my $idx (0..($numOfEdges - 1)) {
	print OUT2 "<edge id=\"$idx\" source=\"${$sortedArr1[$idx]}[0].0\" ".
	"target=\"${$sortedArr1[$idx]}[1].0\" weight=\"${$sortedArr1[$idx]}[2]\"/>\n";
}
print OUT2 "</edges>\n";
print OUT2 "</graph>\n";
print OUT2 "</gexf>\n";
close(OUT2);

#print "arr1:\n";
#foreach my $i (0..20) {
#	print "@{$sortedArr1[$i]}\n";
#}
#print "arr2:\n";
#foreach my $i (0..20) {
#	print "@{$sortedArr2[$i]}\n";
#}
open(OUT, ">dependency.wpairs");
my $pointer1 = 0;
my $pointer2 = 0;
my $value1 = 0;
my $value2 = 0;
my $value3 = 0;
my $flag = 0;
#print "${$arr1[$pointer1]}[0]\n";
while ($pointer1 <= $#sortedArr1 || $pointer2 <= $#sortedArr2) {
	#print "$pointer1\t$pointer2\n";
	#print "$#arr1\t$#arr2\n";
	$flag = 0;
	if ($pointer1 > $#sortedArr1 && $pointer2 <= $#sortedArr2) {
		$value1 = ${$sortedArr2[$pointer2]}[0];
		$value2 = ${$sortedArr2[$pointer2]}[1];
		$value3 = ${$sortedArr2[$pointer2]}[2];
		#print OUT "${$sortedArr2[$pointer2]}[0]\t${$sortedArr2[$pointer2]}[1]\t${$sortedArr2[$pointer2]}[2]\n";
		$pointer2 += 1;
		$flag = 1;
	} elsif ($pointer1 <= $#sortedArr1 && $pointer2 > $#sortedArr2) {
		$value1 = ${$sortedArr1[$pointer1]}[0];
		$value2 = ${$sortedArr1[$pointer1]}[1];
		$value3 = ${$sortedArr1[$pointer1]}[2];
		#print OUT "${$sortedArr1[$pointer1]}[0]\t${$sortedArr1[$pointer1]}[1]\t${$sortedArr1[$pointer1]}[2]\n";
		$pointer1 += 1;
		$flag = 1;
	}
	if (!$flag && ${$sortedArr1[$pointer1]}[0] < ${$sortedArr2[$pointer2]}[0]) {
		$value1 = ${$sortedArr1[$pointer1]}[0];
		$value2 = ${$sortedArr1[$pointer1]}[1];
		$value3 = ${$sortedArr1[$pointer1]}[2];
		#print OUT "${$sortedArr1[$pointer1]}[0]\t${$sortedArr1[$pointer1]}[1]\t${$sortedArr1[$pointer1]}[2]\n";
		$pointer1 += 1;
		#print OUT "1\n";
	} elsif (!$flag && ${$sortedArr1[$pointer1]}[0] > ${$sortedArr2[$pointer2]}[0]) {
		$value1 = ${$sortedArr2[$pointer2]}[0];
		$value2 = ${$sortedArr2[$pointer2]}[1];
		$value3 = ${$sortedArr2[$pointer2]}[2];
		#print OUT "${$sortedArr2[$pointer2]}[0]\t${$sortedArr2[$pointer2]}[1]\t${$sortedArr2[$pointer2]}[2]\n";
		$pointer2 += 1;
		#print OUT "2\n";
	} else {
		if (!$flag && ${$sortedArr1[$pointer1]}[1] < ${$sortedArr2[$pointer2]}[1]) {
			$value1 = ${$sortedArr1[$pointer1]}[0];
			$value2 = ${$sortedArr1[$pointer1]}[1];	
			$value3 = ${$sortedArr1[$pointer1]}[2];		
			#print OUT "${$sortedArr1[$pointer1]}[0]\t${$sortedArr1[$pointer1]}[1]\t${$sortedArr1[$pointer1]}[2]\n";
			$pointer1 += 1;
		} elsif (!$flag && ${$sortedArr1[$pointer1]}[1] >= ${$sortedArr2[$pointer2]}[1]) {
			$value1 = ${$sortedArr2[$pointer2]}[0];
			$value2 = ${$sortedArr2[$pointer2]}[1];
			$value3 = ${$sortedArr2[$pointer2]}[2];
			#print OUT "${$sortedArr2[$pointer2]}[0]\t${$sortedArr2[$pointer2]}[1]\t${$sortedArr2[$pointer2]}[2]\n";
			$pointer2 += 1;
		} 
	}
	#$value1 -= 1;
	#$value2 -= 1;
	print OUT "$value1\t$value2\t$value3\n";

}
close(OUT);

# Community Detection
# We will get a file called "level" including all communities and
# corresponding nodes
system("perl communityDetection.pl");
my %comm2node;
open(IN, "level");
while(<IN>) {
	chomp;
	if (/(\d+) (\d+)/) {
		my $node = $1;
		my $community = $2;
		push @{$comm2node{$community}}, $node;
	}
}
close(IN);

my $max = 0;
foreach my $community (keys %comm2node) {
	next if ($#{$comm2node{$community}} < 100);
	$max = $#{$comm2node{$community}} if ($#{$comm2node{$community}} > $max);
}
print "max = $max\n";