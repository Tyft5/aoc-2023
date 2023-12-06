#include <iostream>
#include <cstdio>
#include <fstream>
#include <string>
#include <vector>
#include <regex>
#include <limits.h>
#include <omp.h>
#include <ctime>
using namespace std;

long dest_from_src(long* mapping, size_t num_lines, long the_id)
{
    long dest, src, span;

    // iterate by 3 since each lines has 3 numbers
    for (int mi = 0; mi < num_lines; mi++)
    {  // for each line/range
	dest = *(mapping + 3*mi);
        src = *(mapping + 3*mi + 1);
        span = *(mapping + 3*mi + 2);

        if ((src <= the_id) && (the_id < (src + span)))
        {
            // the id is in range, get the dest id
            return (dest + (the_id - src));
        }
    }

    // id wasn't in any ranges, so it's 1 to 1
    return the_id;
}

long get_location(long* data, size_t* map_sizes, size_t mps_len, long the_id)
{
    size_t jump {0};
    int doffset {0};

    for (int m = 0; m < mps_len; m++)
    { // for each mapping
	// get the destination id from the source id
	// there are 3 numbers on each line
	doffset += m ? 3*jump : 0;
      	jump = *(map_sizes + m);
	the_id = dest_from_src(data + doffset, jump, the_id);
    }

    return the_id;
}

int main(int argc, char* argv[])
{
    long seed_start, seed_span;
    long min_dist {LONG_MAX};

    vector<long> seeds, indata;

    size_t map_lines {0};
    vector<size_t> map_sizes;

    string line{}, seedstr{}, aseed{};
    size_t pos {0};
    smatch match;

    ifstream infile (argv[1]);

    regex num_ptrn {"\\d+"};
    regex map_ptrn {"map"};

    // sanity check
    cout << "Devices: " << omp_get_num_devices() << endl;

    omp_set_num_threads(1);

    time_t start_t;
    time(&start_t);

    if (infile.is_open())
    {
        // grab seeds from first line
        getline(infile, line);
        seedstr = line.substr(line.find(":")+2, line.length());
        while ((pos = seedstr.find(" ")) != string::npos)
        {
            aseed = seedstr.substr(0, pos);
            seeds.push_back(stol(aseed));
            seedstr.erase(0, pos + 1);
        }
        // grab the last seed, which is all that remains (no spaces)
        seeds.push_back(stoi(seedstr));

        while (getline(infile, line))
        {
            // skip empty lines
            if (line.size() == 0) {}
            else if (regex_search(line, map_ptrn))
            {
                // new map tier
		if (map_lines)
		    map_sizes.push_back(map_lines);
		map_lines = 0;
            }
            else
            {
                // build data structure:
                while (regex_search(line, match, num_ptrn))
                {
                    // line has numbers, loop through them and add to the vector
		    indata.push_back(stol(match[0]));
                    line = match.suffix().str();
                }
		map_lines++;
            }
        }

	// get last map size
	map_sizes.push_back(map_lines);
    }

    // we have to prepare the data for sending to the GPU, it doesn't like vectors
    long* datarr = indata.data();
    long* seedsarr = seeds.data();
    size_t* map_sz_arr = map_sizes.data();

    size_t num_maps = map_sizes.size();
    size_t num_seeds = seeds.size();

    cout << "Input read took " << time(NULL) - start_t << " s" << endl;
    time(&start_t);

// allocate and send data to the GPU
#pragma omp target enter data \
    map(to:seedsarr[:seeds.size()],datarr[:indata.size()],map_sz_arr[:map_sizes.size()])

// on the GPU; min_dist is tofrom so it gets updated on the host
#pragma omp target map(tofrom:min_dist)
{
    // Split the seeds among teams, with a min reduction to combine them
    //#pragma omp teams num_teams(num_seeds/2) reduction(min : min_dist)
    #pragma omp teams reduction(min : min_dist)
	
    {
	long dist;
	#pragma omp distribute
    	for (int i = 0; i < num_seeds; i += 2)
    	{
            seed_start = seedsarr[i];
       	    seed_span = seedsarr[i + 1];

	    // Split seed exploration among threads, again with a min reduction
	    #pragma omp parallel for reduction(min : min_dist) private(dist)
            for (long s = seed_start; s < seed_start + seed_span; s++)
            {
                dist = get_location(datarr, map_sz_arr, num_maps, s);

                if (dist < min_dist)
                    min_dist = dist;
            }
	}
    }
}

    cout << "Brute forcing took " << time(NULL) - start_t << " s" << endl;

    cout << "Part 2: " << min_dist << endl;

    return 0;
}
