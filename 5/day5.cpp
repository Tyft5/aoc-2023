#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <regex>
#include <limits.h>
using namespace std;

long dest_from_src(vector<vector<long>> mapping, long the_id)
{
    long dest, src, span;

    for (const auto& mp : mapping)
    {  // for each line/range
        dest = mp[0];
        src = mp[1];
        span = mp[2];

        if ((src <= the_id) && (the_id < (src + span)))
        {
            // the id is in range, get the dest id
            return (dest + (the_id - src));
        }
    }

    // id wasn't in any ranges, so it's 1 to 1
    return the_id;
}

long get_location(vector<vector<vector<long>>> data, long the_id)
{
    for (const auto& m : data)
    { // for each mapping
        the_id = dest_from_src(m, the_id);
    }
    return the_id;
}

int main(int argc, char* argv[])
{
    long seed_start, seed_span, dist;
    long min_dist {LONG_MAX};

    vector<long> line_nums, seeds;
    vector<vector<long>> map_nums;
    vector<vector<vector<long>>> data;

    string line{}, seedstr{}, aseed{};
    size_t pos {0};
    smatch match;

    ifstream infile (argv[1]);

    regex num_ptrn {"\\d+"};
    regex map_ptrn {"map"};

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
                // store and reset the map number vectors
                data.push_back(map_nums);
                map_nums = vector<vector<long>>();
            }
            else
            {
                // build data structure:
                // [ #map [ #range ( destination, source, span ), ... ], ... ]
                line_nums = vector<long>();
                while (regex_search(line, match, num_ptrn))
                {
                    // line has numbers, loop through them and add to the vector
                    line_nums.push_back(stol(match[0]));
                    line = match.suffix().str();
                }

                // add line numbers to this map's vector
                map_nums.push_back(line_nums);
            }
        }
    }

    for (int i = 0; i < seeds.size(); i += 2)
    {
        seed_start = seeds[i];
        seed_span = seeds[i+1];

        for (long s = seed_start; s < seed_start + seed_span; s++)
        {
            dist = get_location(data, s);

            if (dist < min_dist)
                min_dist = dist;
        }
    }

    cout << "Part 2: " << min_dist << endl;

}
