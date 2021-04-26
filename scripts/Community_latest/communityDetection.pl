system("make");
system("rm -f graph.tree level6");
system("./community 200 0 0 graph.bin -l -1 -w graph.weights > graph.tree");
system("./hierarchy graph.tree > temp_hier");
my $lastLevel = 0;
open(IN, "temp_hier");
while(<IN>) {
	chomp;
	$lastLevel = $1 if (/level (\d+): \d+ nodes/);
}
system("./hierarchy graph.tree -l $lastLevel > level$lastLevel");
rm("rm -f temp_hier");