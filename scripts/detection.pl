no warnings 'experimental::smartmatch';
use strict;
use warnings;

system("make");
system("rm -f graph.tree level");
system("./convert -i dependency.wpairs -o graph.bin -w graph.weights");
system("./community 16 0 0 graph.bin -l -1 -w graph.weights > graph.tree");
system("./hierarchy graph.tree > temp_hier");
my $lastLevel = 0;
my $numNodes = 0;
open(IN, "temp_hier");
while(<IN>) {
	chomp;
	if (/level (\d+): (\d+) nodes/) {
		$lastLevel = $1;
		$numNodes = $2;
	}
}
print "numOfNodes = $numNodes\n";
#$lastLevel -= 1;
#system("./hierarchy graph.tree -l $lastLevel > level");
system("./hierarchy graph.tree -l $lastLevel > level");
#system("rm -f temp_hier");
my %comm2node;
my @order;
open(IN, "level");
while(<IN>) {
	chomp;
	if (/(\d+) (\d+)/) {
		my $node = $1;
		my $community = $2;
		push @{$comm2node{$community}}, $node;
		if (! ($community ~~ @order)) {
			push @order, $community;
		}
	}
}
close(IN);
my @arr;
my @sortedOrder = sort {$a <=> $b} @order;
foreach my $community (@sortedOrder) {
	next if ($#{$comm2node{$community}} < 2); #5 if qSort, 2 otherwise
	push @arr, $#{$comm2node{$community}}  if ($#{$comm2node{$community}} >= 0);
}
my $max = 0;
print "arr = @arr\n";
print "num of cluster = $#arr\n";
foreach my $weightIndex (0..($#arr-1)) {
	$max += abs(($arr[$weightIndex] - $arr[($weightIndex + 1)]));
}
print "max = $max\n";