@echo off

python stage-boss-one-profile.py --no 10 --dir c:\working\droid-test\govdocs > govdocs-analysis.csv

timeout 10

python stage-boss-one-profile.py --no 10 --dir c:\working\droid-test\fake_govdocs > fake_govdocs-analysis.csv

timeout 10

python stage-boss-one-profile.py --no 10 --dir c:\working\droid-test\wavs > wavs-analysis.csv

timeout 10

sf -sig "C:\working\git\digital-preservation-stage-boss-one\siegfried.sigs\container\NOLIMIT-1.6.2-v86-july2016-default.sig" c:\working\droid-test\govdocs > sf-container-NOLIMIT.sf

timeout 10

sf -sig "C:\working\git\digital-preservation-stage-boss-one\siegfried.sigs\no-container\NOLIMIT-1.6.2-v86-july2016-nocontainer-default.sig" c:\working\droid-test\govdocs > sf-no-container-NOLIMIT.sf

timeout 10

sf -sig "C:\working\git\digital-preservation-stage-boss-one\siegfried.sigs\container\10MB-1.6.2-v86-july2016-default.sig" c:\working\droid-test\govdocs > sf-container-10MB.sf

timeout 10

sf -sig "C:\working\git\digital-preservation-stage-boss-one\siegfried.sigs\no-container\10MB-1.6.2-v86-july2016-nocontainer-default.sig" c:\working\droid-test\govdocs > sf-no-container-10MB.sf

timeout 10

sf -sig "C:\working\git\digital-preservation-stage-boss-one\siegfried.sigs\container\65535-1.6.2-v86-july2016-default.sig" c:\working\droid-test\govdocs > sf-container-65535.sf

timeout 10

sf -sig "C:\working\git\digital-preservation-stage-boss-one\siegfried.sigs\no-container\65535-1.6.2-v86-july2016-nocontainer-default.sig" c:\working\droid-test\govdocs > sf-no-container-65535.sf

timeout 10