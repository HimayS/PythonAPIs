1> run tika-server to get the content from file: java -jar tika-server-standard-2.9.2.jar
By default tika server port is 9998, but you can modify it using --port XXXX

2> generate groq api from https://console.groq.com/keys
and replace it in agents.py file.

3> install python library of crewai: pip install crewai