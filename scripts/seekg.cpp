#include <iostream>
#include <fstream>
using namespace std;

int main() {
	std::ifstream is ("a.out_ct.link.bc", std::ifstream::binary);
	if (is) {
		is.seekg (0, is.end);
		int length = is.tellg();
		cout << "length is " << length << endl;
		is.seekg (0, is.beg);
		char * buffer = new char [length];
		is.read(buffer, length);
		is.close();
		std::cout.write(buffer, length);
		delete[] buffer;
	}
	return 0;
}