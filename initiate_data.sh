#!/usr/bin/env bash
echo "Now you are constructing the database...Please make sure that your MongoDB service is open.";
sed -i 's/\r$//' ./initiate_data.sh;
mongoimport --db felkub --collection directors --file ./datas/directors.json;
mongoimport --db felkub --collection movies --file ./datas/movies.json;
mongoimport --db felkub --collection starring --file ./datas/starring.json;
mongoimport --db felkub --collection tags --file ./datas/tags.json;
mongoimport --db felkub --collection genres --file ./datas/genres.json;