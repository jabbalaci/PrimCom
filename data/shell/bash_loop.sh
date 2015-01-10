for i in *.mp3; do echo `basename "$i" .mp3`; done

for i in {1..5}; do echo $i; done

for i in $( ls ); do echo $i; done
for line in $( cat test.txt ); do echo $line; done

find . | grep mp3 | while read i; do echo $i; done

while :; do echo y; sleep 1; done    # infinite loop
