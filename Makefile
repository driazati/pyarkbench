test_data:
	python ./benchmarks/test.py --runs 3 --out driazati.github.io/ --time "2019-11-08T17:16:50-08:00" --pr "12346" --hash "9f917abed18833ac00577844fe13375ac8fce168"
	python ./benchmarks/test.py --runs 3 --out driazati.github.io/ --time "2019-11-07T17:16:50-08:00" --pr "12345" --hash "8f917abed18833ac00577844fe13375ac8fce168"
	python ./benchmarks/test.py --runs 3 --out driazati.github.io/ --time "2019-11-09T17:16:50-08:00" --pr "12347" --hash "af917abed18833ac00577844fe13375ac8fce168"
	python ./benchmarks/test.py --runs 3 --out driazati.github.io/ --time "2019-11-10T17:16:50-08:00" --pr "12348" --hash "bf917abed18833ac00577844fe13375ac8fce168"
	python ./benchmarks/test.py --runs 3 --out driazati.github.io/ --time "2019-11-11T17:16:50-08:00" --pr "12345" --hash "cf917abed18833ac00577844fe13375ac8fce168"
	python ./benchmarks/test.py --runs 3 --out driazati.github.io/ --time "2019-11-12T17:16:50-08:00" --pr "12345" --hash "df917abed18833ac00577844fe13375ac8fce168"
	python ./benchmarks/test.py --runs 3 --out driazati.github.io/ --time "2019-11-13T17:16:50-08:00" --pr "12345" --hash "ef917abed18833ac00577844fe13375ac8fce168"
	python ./benchmarks/test.py --runs 3 --out driazati.github.io/ --time "2019-11-14T17:16:50-08:00" --pr "12345" --hash "ff917abed18833ac00577844fe13375ac8fce168"
	python ./benchmarks/test.py --runs 3 --out driazati.github.io/ --time "2019-11-15T17:16:50-08:00" --pr "12345" --hash "gf917abed18833ac00577844fe13375ac8fce168"


clean:
	rm -f driazati.github.io/basic.json basic.json