@echo off

python stage-boss-one-profile.py --no 10 --dir c:\working\droid-test\wavs > wavs-analysis.csv

timeout 10

python stage-boss-one-profile.py --no 10 --dir c:\working\droid-test\fake_govdocs > fake_govdocs-analysis.csv

timeout 10

python stage-boss-one-profile.py --no 10 --dir c:\working\droid-test\govdocs > govdocs-analysis.csv

timeout 10