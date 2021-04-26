open(IN1, "../../traj_planning/c_code/main.cpp.ll");

my $counter = 0;
my %counter2Instr;
while(<IN1>) {
	chomp;
	$counter2Instr{$counter} = $_;
	$counter++;
}

open(IN2, "level");
my %comm2Instr;
my %instr2Comm;
while(<IN2>) {
	chomp;
	if (/(\d+) (\d+)/) {
		my $node = $1;
		my $community = $2;
		push @{$comm2Instr{$community}}, $counter2Instr{$node};
		$instr2Comm{$1} = $2;
	}
}

close(IN1);
close(IN2);

my $i = 0;
foreach my $index (keys %comm2Instr) {
	open(OUT, ">../../traj_planning/c_code/c128/drone.ll-$i");
	foreach my $ins (@{${comm2Instr}{$index}}) {
		print OUT "$ins\n";
	}
	$i++;
	close(OUT);
}

open(IN3, "../../traj_planning/c_code/main.cpp-dependency.wpairs");
my $totalCost = 0;
while(<IN3>) {
	chomp;
	#print;
	if (/(\d+)\s+(\d+)\s+(\d+)/) {
		#print "HAHA\n";
		my $node1 = $1;
		my $node2 = $2;
		my $cost  = $3;
		#print "node 1 comm $instr2Comm{$1}\n";
		#print "node 2 comm $instr2Comm{$2}\n";
		if ($instr2Comm{$1} != $instr2Comm{$2}) {
			$totalCost += $cost;
			#print "HAHA\n";
		}
	}
}
print "total communication cost is $totalCost.\n";

close(IN3);
