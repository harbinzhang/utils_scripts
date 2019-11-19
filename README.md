# utils_scripts

## maven-dep-version-check.py
check if maven-dep-version is trusted compared to `jars.csv`.
Using full text compare, just like the way how people find and compare the package and version. Which should be fine, no package would be missed, but the time complexity is worse though.
