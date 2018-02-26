#include <bits/stdc++.h>
#include <string.h>
using namespace std;

int main(int argc, char* argv[])
{
    int n;
	char *p;

	string ratings = argv[1];
    string index = argv[2];
	string line;
	ifstream myfile1(ratings);

	int cnt = 0;
	string cur = "";
    string prev = "";
    ofstream outputFile1(index + "_train_ratings.txt");
    ofstream outputFile2(index + "_test_ratings.txt");
    vector<string> vec;
	if (myfile1)
    {
    	while (getline( myfile1, line ))  // same as: while (getline( myfile, line ).good())
    	{
            if(cnt == 0) {
                outputFile1 << line << "\n";
                outputFile2 << line << "\n";
            }
    		else if(cnt > 0) {
                size_t pos = line.find(",");
                cur = line.substr(0,pos);

                if(cur.compare(prev) != 0){
                    prev = cur;
                    random_shuffle ( vec.begin(), vec.end() );
                    int n = vec.size();
                    for(int i=0; i<n/2; i++)
                        outputFile1 << vec[i] << "\n";
                    for(int i=n/2; i<n; i++)
                        outputFile2 << vec[i] << "\n";

                    vec.clear();
                    vec.push_back(line);
                }
                else {
                    prev = cur;
                    vec.push_back(line);
                }
    		}

    		cnt++;
    	}
    	myfile1.close();
        random_shuffle ( vec.begin(), vec.end() );
        int n = vec.size();
        for(int i=0; i<n/2; i++)
            outputFile1 << vec[i] << "\n";
        for(int i=n/2; i<n; i++)
            outputFile2 << vec[i] << "\n";

        vec.clear();   
    }
    else	cout << "Error opening the rating file\n";
}
