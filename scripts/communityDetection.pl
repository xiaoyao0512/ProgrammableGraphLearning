system("make");
system("rm -f graph.tree level");
system("./convert -i ../../traj_planning/c_code/main.cpp-dependency.wpairs -o graph.bin -w graph.weights");
# N(estimated number of cores) lambda1(load balancing, cluster has similar instructions) lambda2(number of communities balancing)
system("./community 128 0 0.5 graph.bin -l -1 -w graph.weights > graph.tree");
system("./hierarchy graph.tree > temp_hier");
my $lastLevel = 0;
open(IN, "temp_hier");
while(<IN>) {
	chomp;
	$lastLevel = $1 if (/level (\d+): \d+ nodes/);
}
system("./hierarchy graph.tree -l $lastLevel > level");
#system("rm -f temp_hier");
