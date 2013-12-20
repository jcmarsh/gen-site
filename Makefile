default:
	python make_site.py web_source generated

clean:
	rm -rf ./generated/*
