#!/usr/bin/perl -w
# This is the most up2date file

use strict;
no warnings 'experimental::smartmatch';

sub add_vertex {
	my $graphRef = shift;
	my $v = shift;
	if (exists ($graphRef->{$v})) {
		#print "Vertex $v already exists.\n";
		;
	} else {
		$graphRef->{$v} = ();
	}
}

sub add_edge {
	my ($graphRef, $v1, $v2, $w) = @_;
	if (not exists ($graphRef->{$v1})) {
		print "Vertex $v1 does not exist.\n";
		exit 0;
	} elsif (not exists ($graphRef->{$v2})) {
		print "Vertex $v2 does not exist.\n";
		exit 0;
	} else {
		my @temp = ($v2, $w);
		push @{$graphRef->{$v1}}, [@temp];
	}
}

sub print_graph {
	#my $graphRef = shift;
	#my $graph = shift;#%{$graphRef};
	my %g = @_;
	#print "graph\n";
	while (my ($v, $e) = each (%g)) {
		if (defined $e) {
			my @edges = @{$e};
			foreach (@edges) {
				print "$v -> ${$_}[0], edge weight: ${$_}[1]\n";
			}
		}
	}
}

sub print_graph_to_gephi {
	#my ($file, %graph, $node, $edge) = @_;
	my $file = shift;
	my $graphRef = shift;
	my $node = shift;
	my $edge = shift;
	open(OUT2, ">graphs/$file.gexf");
	print OUT2 "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n";
	print OUT2 "<gexf xmlns:viz=\"http://www.gexf.net/1.1draft/viz\" ",
	"version=\"1.1\" xmlns=\"http://www.gexf.net/1.1draft\">\n";
	print OUT2 "<meta lastmodifieddate=\"2020-05-08+6:30\">\n";
	print OUT2 "<creator>Gephi 0.7</creator>\n";
	print OUT2 "</meta>\n";
	print OUT2 "<graph defaultedgetype=\"directed\" idtype=\"string\" ",
	"type=\"static\">\n";
	print OUT2 "<nodes count=\"$node\">\n";
	foreach my $n (keys %{$graphRef}) {
		print OUT2 "<node id=\"$n\" label=\"$n\"/>\n";
	}
	print OUT2 "</nodes>\n";
	print OUT2 "<edges count=\"$edge\">\n";
	my $counter = 0;
	while (my ($n, $links) = each (%{$graphRef})) {
		if (defined $links) {
			#print "links = $links\n";
			my @link = @{$links};
			#print "@link\n";
			foreach my $e (@link) {
				my $target = ${$e}[0];
				my $w = ${$e}[1];
				print OUT2 "<edge id=\"$counter\" source=\"$n\" target=\"$target\" weight=\"$w\"/>\n";
				$counter += 1;
			}
		}
	}
	print OUT2 "</edges>\n";
	print OUT2 "</graph>\n";
	print OUT2 "</gexf>\n";
	close(OUT2);
}


sub print_graph_to_netX {
	#my $graphRef = shift;
	#my $graph = shift;#%{$graphRef};
    my $file = shift;
    my $graphRef = shift;
    substr($file, -2) = '';
    $file =~ s/-/_/g;
    $file =~ s/\./_/g;
	#print "graph\n";
    print "$file\n";
    open(OUT2, ">graphs/$file.py");
    print OUT2 "import networkx as nx\n";
    print OUT2 "import dgl\n";
    print OUT2 "def $file():\n";
    print OUT2 "\tNXG = nx.DiGraph()\n"; #DiGraph()
    
	while (my ($v, $e) = each (%{$graphRef})) {
		if (defined $e) {
			#print "links = $links\n";
			my @edges = @{$e};
			#print "@link\n";
			foreach my $edge (@edges) {
				my $target = ${$edge}[0];
				my $w = ${$edge}[1];
				print OUT2 "\tNXG.add_edge($v, $target, weight=$w)\n";
                print OUT2 "\tNXG.add_node($v, w=$w)\n";
                print OUT2 "\tNXG.add_node($target, w=$w)\n";
			}
		}
	}
    
    #print OUT2 "\tg = dgl.graph()\n";
    print OUT2 "\tg = dgl.from_networkx(NXG, edge_attrs=['weight'], node_attrs=['w'])\n";
    print OUT2 "\treturn g\n";
    #print OUT2 "\treturn g\n";
    #print OUT2 "print(nx.is_connected(G))\n\n\n";
    close(OUT2);
}



sub print_graph_to_netX_wSelfLoops {
	#my $graphRef = shift;
	#my $graph = shift;#%{$graphRef};
    my $file = shift;
    my $graphRef = shift;
    my $node = shift;
    substr($file, -2) = '';
    $file =~ s/-/_/g;
    $file =~ s/\./_/g;
	#print "graph\n";
    print "$file\n";
    open(OUT2, ">graphs/$file.py");
    print OUT2 "import networkx as nx\n";
    print OUT2 "import dgl\n";
    print OUT2 "def $file():\n";
    print OUT2 "\tNXG = nx.DiGraph()\n"; #DiGraph()
    my %nodes;
	while (my ($v, $e) = each (%{$graphRef})) {
		if (defined $e) {
			#print "links = $links\n";
			my @edges = @{$e};
			#print "@link\n";
			foreach my $edge (@edges) {
				my $target = ${$edge}[0];
				my $w = ${$edge}[1];
				print OUT2 "\tNXG.add_edge($v, $target, weight=$w)\n";
                if (defined $nodes{$v}) {
                    $nodes{$v} += $w; 
                } else {
                    $nodes{$v} = $w;
                }
                if (defined $nodes{$target}) {
                    $nodes{$target} += $w; 
                } else {
                    $nodes{$target} = $w;
                }
                #print OUT2 "\tNXG.add_node($v, w=$w)\n";
                #print OUT2 "\tNXG.add_node($target, w=$w)\n";
			}
		}
	}
    # adding self loops
	foreach my $n (keys %{$graphRef}) {
		print OUT2 "\tNXG.add_edge($n, $n, weight=1)\n";
	}
    # add node attributes
	foreach my $n (keys %nodes) {
        my $v = $nodes{$n};
		print OUT2 "\tNXG.add_node($n, w=$v)\n";
	}
    #print OUT2 "\tg = dgl.graph()\n";
    print OUT2 "\tg = dgl.from_networkx(NXG, edge_attrs=['weight'], node_attrs=['w'])\n";
    print OUT2 "\treturn g\n";
    #print OUT2 "\treturn g\n";
    #print OUT2 "print(nx.is_connected(G))\n\n\n";
    close(OUT2);
}


my $ARGC = scalar @ARGV;
if ($ARGC < 1) {
	print "\nusage: perl run.pl <a file you want to instrument> <arguments required by the file>\n\n";
	exit 1;
}

my $file = $ARGV[0];
my @arguments = @ARGV[1..$ARGC - 1];
#print "arguments: @arguments\n";
my %BBs;
my $index = -1;
my $BB = 0;
my @global;
my @str;
###################Instrument the file##############################
my $numOfStr = 0;
my $isStr = 0;
my $isPrinted = 0;
my $doNotPrint = 0;
my $numOfSL = 0;
my $main = 0;
my $hasPrint = 0;
my %func;
my %callFunc;

system("clang -emit-llvm -S -c $file -o llvm.ll -Wmain-return-type");

open(IN, "llvm.ll");
open(OUT, ">llvm_instrumented.ll");

while (<IN>) {
	chomp;
	if (/define \w+ \@(.*)\((.*)\)/) {
		#print "$2\n";
		my $fncName = $1;
		#print "qwert\t$1\n";
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
	}
	#if (/call .* \@(.*)\((.*)\)/) {
		#print "$2\n";
	#	my $fncName = $1;
	#	my @args = split /,/, $2;
		#print "args: $#args\n";
		#print "@args\n";
		#push @{$func{$1}}, ($#args + 1);
	#	push @{$callFunc{$fncName}}, @args;
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
	#}
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
		print OUT "\@.str." . "$numOfStr" ." = private unnamed_addr constant [17 x i8] c\"counter is %lli\\0A\\00\", align 1\n";
		$isPrinted = 1;
	}
	if (/; Function Attrs:/ && !$isPrinted && !$doNotPrint) {
		print OUT "\@.str.$numOfStr = private unnamed_addr constant [17 x i8] c\"counter is %lli\\0A\\00\", align 1\n\n";
		$doNotPrint = 1;
	}
	if (/store|load/) { #before load/store instr, instrument rdsc()
		$numOfSL++;
		#print OUT "  %SL" . "$numOfSL" . " = call i64 \@rdtsc()\n";
	}
	print OUT;
	print OUT "\n";

	if (/store|load/) {
		$numOfSL++;
		#print OUT "  %SL" . "$numOfSL" . " = call i64 \@rdtsc()\n";
		$numOfSL++;
		my $temp1 = $numOfSL - 1;
		my $temp2 = $numOfSL - 2;
		#print OUT "  %SL" . "$numOfSL" . " = sub i64 %SL$temp1, %SL$temp2\n";
		$numOfSL++;
		$temp1 = $numOfSL - 1;
		#print OUT "  %SL$numOfSL = call i32 (i8*, ...) \@printf(i8* getelementptr inbounds ([17 x i8], [17 x i8]* \@.str.$numOfStr, i32 0, i32 0), i64 %SL$temp1)\n";	
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

########################END#########################################
#print "str = @str\n";

my @timing;
my @printf;
#system("lli llvm_instrumented.ll @arguments > timing");
#if (defined $ARGV[1]) {
#	system("lli llvm_instrumented.ll $ARGV[1] > timing");
# else {
#	system("lli llvm_instrumented.ll > timing");
#}
#open(IN, "timing");
#while(<IN>) {
#	chomp;
#	if (/counter is (\d+)/) {
#		unshift @timing, $1;
#	} else {
#		unshift @printf, $_;
#	}
#}


close(IN);

system("rm -f output/*");
system("nice -n -19 ./contech_wrapper_par.py $file -lm -Wmain-return-type > log");
my $currentFunctionName;
my @skipStore;
my $br = 0;
my %funcIndex; #$func
my $bbIdx = -1;

open(IN, "log");
while (<IN>) {
	chomp;
	if (/call .* \@(.*)\((.*)\)/) {
		#print "callFunc: $1\t$2\n";
		my $fncName = $1;
		#my @args = split /,/, $2;
        my $args = $2;
		#print "args: $#args\n";
		#print "@args\n";
        #print "bbidx : $bbIdx\n";
		#push @{$func{$1}}, ($#args + 1);
        next if ($fncName =~ /stacksave/);
        #print "callFunc: $fncName->$args\t----$bbIdx\n";
		push @{$callFunc{$fncName}}, [$args, $bbIdx];
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
	} 
    $bbIdx++ if (/#BasicBlock/)
}
close(IN);
my $fff = "WT_estimator_v3";
#print "-------$fff--------\n";

#print "%func\n";
my $var = "WT_estimator_v3";
#print "@{$func{$var}}\n";


open(IN, "log");
while (<IN>) {
	chomp;
	if (/current function name: (\w+)/) {
		$currentFunctionName = $1;
        #print "currFunc: $currentFunctionName \n";
		next if ($currentFunctionName eq "main");
		#my $bbAhead = $index + 1;
		foreach my $i (0..$#{$func{$currentFunctionName}}) {
			#print "i = $i\n";
			#print "$currentFunctionName: \n";
			#print "${$func{$currentFunctionName}}[$i] - ${$callFunc{$currentFunctionName}}[$i]\n";
			my @temp1;
			${$func{$currentFunctionName}}[$i] =~ s/^\s*//;
			my $flag1 = 0;
			my $flag2 = 0;
			if (${$func{$currentFunctionName}}[$i] =~ /^%/) {
				@temp1 = split / +/, ${$func{$currentFunctionName}}[$i];
				$flag1 = 1;
			} else {
				@temp1 = split /%/, ${$func{$currentFunctionName}}[$i];
				$flag2 = 1;
			}
			$temp1[0] =~ s/\s+$//;
            foreach my $argPlusIdx (@{$callFunc{$currentFunctionName}}) {
                #print "argPlusIdx: $argPlusIdx->[0]\t$argPlusIdx->[1]\n";
                my $bbAhead = $argPlusIdx->[1];
                my @temp2 = split /,/, ($argPlusIdx->[0]);
                #print "-------bbahead = $bbAhead--------\n";
			    #print "funcname : $currentFunctionName\t@temp2\t$bbAhead\n";
			    if (defined $temp2[$i]) {
				    if ($flag2) {
                        #print "flag2\n";
					    push @skipStore, "store $temp2[$i], $temp1[0]* \%$temp1[1], align 8";
					    push @{$BBs{$bbAhead}}, "store $temp2[$i], $temp1[0]* \%$temp1[1], align 8";
				    } elsif ($flag1) {
                        #print "flag1\n";
					    push @skipStore, "store $temp2[$i], $temp1[0]* $temp1[1], align 8";
					    push @{$BBs{$bbAhead}}, "store $temp2[$i], $temp1[0]* $temp1[1], align 8";			
				    }
			    }
                #last;
            }
		}
	}
	if (/\%(\d+) = call.*@/) {
		my $num = int($1) + 1;
		#print $_, "\n";
		$_ =~ s/%(\d+) = call/%$num = call/;
		#print $_, "\n";
	}
	if ($BB) {
		#if ($currentFunctionName ~~ keys %func)
		#push @{$BBs{$index}}, $_ unless (/br|#BasicBlock|END|ret|current|SKIP/);
        if (/load|sitofp|getelementptr/) {
            unshift @{$BBs{$index}}, $_; 
            next;
        }
		push @{$BBs{$index}}, $_ unless (/#BasicBlock|END|current|SKIP|is struct|ret|br/);
		#push @{$BBs{$index}}, $_ if $br;
		#print "$_\n" if (/br/);
		#print;
		#print "\n";
	}
	if (/#BasicBlock/) {
		$index++;
		$BB = 1;
		#print "--------------BB: $index---------------\n";
	}
	if (/END/) {
		$BB = 0;
	}
}	
close(IN);

#print %BBs;
#print "#BB : $index\n";

# Remove control dependencies
# meaning br+cmp should be completely removed from BBs
# reverse order using pop(array)
=comment
while (my ($bb, $instrs) = each %BBs) {
    print "bb: $bb\n:";
    print "\tinstr in bb:\n";
    for my $instr (@{$instrs}) {
        print "\tinstr: $instr\n";
    }
	my $cnt = 0;
	my $control = 0;
	for my $instr (reverse @{$instrs}) {
		if ($instr =~ /br/ and $cnt == 0) {
			# br is the first instruction
			$control += 1;
		} elsif ($instr =~ /cmp/ and $cnt == 1) {
			# cmp is the second instruction
			$control += 1;			
		}
		$cnt += 1;
	}
}
aa=cut
while (my ($bb, $instrs) = each(%BBs)) {
	if (${$instrs}[-1] =~ /cmp/) {
		delete $BBs{$bb};
        print "$bb\n";
	}
}


=comment
#print "global: @global\n";
#@printf;
open(OUT, ">temp.ll");

foreach my $instruction (@str) {
	#print "$instruction\n";
	if ($instruction =~ /c\"(.*)\"/) {
		my $match = $1;
		$match =~ s/\\0A|\\00|\\09|\\\d\w|\\\w\d|\\\d\d/ /gi;
		$match =~ s/^\s+|\s+$//g;
		$match =~ s/\.$//g;
		#print "match = $match\n";
		my @str1 = split / +/, $match;
		#print "str1 = @str1\n";
		foreach my $ins (@printf) {
			my $counter1 = 0;
			my $counter2 = 0;
			$ins =~ s/^\s+|\s+$//g;
			my @str2 = split / +/, $ins;
			#print "str2 = @str2\n";
			foreach my $i (0..$#str2) {
				$counter1++;
				if (defined $str1[$i] && defined $str2[$i] && $str1[$i] =~ /%d/ && $str2[$i] =~ /\d+/) {
					$counter2++;
				} elsif (defined $str1[$i] && defined $str2[$i] && $str1[$i] =~ /%f/ && $str2[$i] =~ /\d*\.\d*/) {
					$counter2++;
				} elsif (defined $str1[$i] && defined $str2[$i] && $str1[$i] =~ /%c/ && $str2[$i] =~ /\w/) {
					$counter2++;
				} elsif (defined $str1[$i] && defined $str2[$i] && $str1[$i] =~ /%s/ && $str2[$i] =~ /\w+/) {
					$counter2++;
				} elsif (defined $str1[$i] && defined $str2[$i] && $str1[$i] eq $str2[$i]) {
					$counter2++;
				}
			}
			#print OUT "$instruction\n";
			print OUT "$instruction\n" if ($counter1 == $counter2);
		}

	}
	
}

foreach my $string (@global) {
	print OUT "$string\n";
}

foreach my $i (0..($index)) {
	foreach my $bb (@{$BBs{$i}}) {
		print OUT "$bb\n";
	}
}

close(OUT);
=cut
#=cut
my @space;
system("./a.out @arguments");
#if (defined $ARGV[1]) {
#	system("./a.out $ARGV[1]");
# else {
#	system("./a.out");
#}
system("nice -n -19 ../middle/middle /tmp/contech_fe Sta > temp");
open(IN, "temp");

open(OUT, ">$file.ll");

=comment
#print "global: @global\n";
foreach my $instruction (@global) {
	print OUT "$instruction\n";
}
foreach my $instruction (@str) {
	#print "$instruction\n";
	if ($instruction =~ /c\"(.*)\"/) {
		my $match = $1;
		$match =~ s/\\0A|\\00|\\09|\\\d\w|\\\w\d|\\\d\d/ /gi;
		$match =~ s/^\s+|\s+$//g;
		$match =~ s/\.$//g;
		#print "match = $match\n";
		my @str1 = split / +/, $match;
		#print "str1 = @str1\n";
		foreach my $ins (@printf) {
			my $counter1 = 0;
			my $counter2 = 0;
			$ins =~ s/^\s+|\s+$//g;
			my @str2 = split / +/, $ins;
			#print "str2 = @str2\n";
			foreach my $i (0..$#str2) {
				$counter1++;
				if (defined $str1[$i] && defined $str2[$i] && $str1[$i] =~ /%d/ && $str2[$i] =~ /\d+/) {
					$counter2++;
				} elsif (defined $str1[$i] && defined $str2[$i] && $str1[$i] =~ /%f/ && $str2[$i] =~ /\d*\.\d*/) {
					$counter2++;
				} elsif (defined $str1[$i] && defined $str2[$i] && $str1[$i] =~ /%c/ && $str2[$i] =~ /\w/) {
					$counter2++;
				} elsif (defined $str1[$i] && defined $str2[$i] && $str1[$i] =~ /%s/ && $str2[$i] =~ /\w+/) {
					$counter2++;
				} elsif (defined $str1[$i] && defined $str2[$i] && $str1[$i] eq $str2[$i]) {
					$counter2++;
				}
			}
			#print "$instruction\n";
			if ($counter1 == $counter2) {
				print OUT "$instruction\n";
				last;
			}
		}

	}
	
}
=cut

while(<IN>) {
	chomp;
	if (/BasicBlock# = (\d+)/) {
		#my $bb = $1;
		if (defined $BBs{$1}) {
			#print OUT "$1:\n";
			for my $instr (@{$BBs{$1}}) {
				print OUT "\t$instr\n";
			}
		} #else {
		#	print "$1:\n";
		#	print "Hey, cannot find the basic block.\n";
		#	print "Something is wrong!\n";
		#	exit 0;
		#}
	}
	#unshift @space, $1 if (/size is (\d+)/);
}
close(OUT);

close(IN);


##################################
# Free some memories
##################################
undef %func;
undef %funcIndex;
undef %callFunc;
undef %BBs;
undef @global;
undef @str;
undef @printf;
##################################


my %graph;

#The graph looks like this:
#graph = {
#
#	"%1" => [["%3", 1], ["%15", 8]],
#	"%4" => [["%6", 4]]
#	...
#}


#add_vertex(\%graph, "1");
#print %graph, "\n";
#my $size = keys %graph;

#add_vertex(\%graph, "n2");
#print %graph, "\n";
#my $size = keys %graph;
#my @t = keys %graph;
#print "size = $size\nitems=@t\n";

#add_edge(\%graph, "1", "n2", 2);
#print %graph, "\n";
#my $size = keys %graph;
#my @t = keys %graph;
#print "size = $size\nitems=@t\n";

#print_graph(%graph);
my %des;
open(IN, "$file.ll");
#open(IN, "test.ll");
#open(IN, "temp.ll");
print "Starting...\n";
my $node = 0;
my $edge = 0;

while(<IN>) {
	chomp;
	#print;
	#print "\n";
	$_ =~ tr/,<>\[\]\(\).//d;
	$_ =~ s/%argc/8/g;
	$_ =~ s/%argv/16/g;
	$_ =~ s/%struct//g;
	my @opcodes = split;
	#print "@opcodes\n";
	my $flag = 0;
	my $desRg;
	my @srcRg;
    next if ($opcodes[0] =~ /Builtin|unreachable/);
	$node += 1;
	add_vertex(\%graph, $node);
	if ($opcodes[0] =~ /%/) {
		# it is an instruction with '='
		# destination register appears on the left
		# side of '='
		for my $op (@opcodes) {
			if ($op =~ /%/ and $flag == 0) {
			# usually destination register
			# since flag = 0
			#print "des: $op\n";
				$desRg = $op;
			} elsif ($op =~ /%/ and $flag == 1) {
			# usually source registers
			# since flag = 1
			#print "source: $op\n";
				push @srcRg, $op;
			} elsif ($op =~ /=/) {
				$flag = 1;
			} 
		}
		# check dependencies, construct graphs
		OUTER: foreach my $s (@srcRg) {
			#print "source: $s\n";
			INNER: foreach my $i (keys %des) {
				if ($s eq $i) {
					add_edge(\%graph, $des{$s}, $node, 1);
					$edge += 1;
					last INNER;
				}
			}
		}
		$des{$desRg} = $node;
	} elsif ($opcodes[0] =~ /store/) {
		# store instruction
		# first/second register are sources;
		# second is dest;
		# But occaionally there's only dest reg.
		my @Rg;
		for my $op (@opcodes) {
			if ($op =~ /%/) {
				#print "$op\n";
				push @Rg, $op;
			}
		}
        #print "Rg: @Rg\n";
		my $size = @Rg;
		if ($size == 1) {
			# one des and one source
			#print "1111\n";
			if (defined $des{$Rg[0]}) {
				#my $time = int(1+rand(8));
				add_edge(\%graph, $des{$Rg[0]}, $node, int(rand(128))+64);				
			}
			$edge += 1;			
			$des{$Rg[0]} = $node;
		} elsif ($size == 2) {
			# two sources one dest
			#print "I am Here\n";
			my $source1 = $Rg[0];
			my $source2 = $Rg[1];
			my $dest = $Rg[1];
			#print "des{source1}: $des{$source1}\n";
			#print "des{source2}: $des{$source2}\n";
			#my $time = int(1+rand(8));
			add_edge(\%graph, $des{$source1}, $node, int(rand(32))+1);
			if (defined $des{$source2}) {
				add_edge(\%graph, $des{$source2}, $node, int(rand(8))+8);
			}
			$edge += 2;			
			$des{$dest} = $node;
		}
	} elsif ($opcodes[0] =~ /call/) {
		# call instruction
		for my $op (@opcodes) {
			if ($op =~ /%/) {	
				#print "$op\n";
				#my $time = int(1+rand(8));
				add_edge(\%graph, $des{$op}, $node, int(rand(64))+1);
				$edge += 1;		
			}
		}
		add_vertex(\%graph, $node+1);
		add_edge(\%graph, $node, $node+1, 1);

	} else {
		print "Sorry, this instruction @opcodes is not recognized.\n";
		print "The program is aborted.\n";
		print "Contact Yao for further mentenance.\n";
		exit 0;
	}
}

close(IN);

undef %des;

#print_graph(%graph);
print("#nodes = $node\n");
print("#edges = $edge\n");
#print_graph_to_gephi($file, \%graph, $node, $edge);
#print_graph_to_netX($file, \%graph, $node);
print_graph_to_netX($file, \%graph);



=comment
open(OUT, ">$file-dependency.wpairs");
open(OUT1, ">$file-assortativity.py");

print OUT1 "#!/usr/bin/python\n\n";
print OUT1 "import networkx as nx\n";
print OUT1 "G = nx.Graph()\n";
print OUT1 "elist = [";
my $pointer1 = 0;
my $pointer2 = 0;
my $value1 = 0;
my $value2 = 0;
my $value3 = 0;
my $flag = 0;
my $counterIter = 0;
#print "${$arr1[$pointer1]}[0]\n";
while ($pointer1 <= $#sortedArr1 || $pointer2 <= $#sortedArr2) {
	#print "$pointer1\t$pointer2\n";
	#print "$#arr1\t$#arr2\n";
	print OUT1 "," if ($counterIter != 0);
	$counterIter++; 
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
	
	##################################################################
	# Calculate the assortativity using networkX in python
	# make sure networkX is properly installed in Ubuntu

	print OUT1 "($value1, $value2, $value3)";
	
}

print OUT1 "]\n";
print OUT1 "G.add_weighted_edges_from(elist)\n";
print OUT1 "r = nx.degree_assortativity_coefficient(G)\n";
print OUT1 "print(\"assortativity coefficient = %3.3f\"%r)\n";

close(OUT);
close(OUT1);
=cut
# Community Detection
# We will get a file called "level" including all communities and
# corresponding nodes

=comment
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

# execute assortativity.py and calculate the coefficient
system("python assortativity.py");
