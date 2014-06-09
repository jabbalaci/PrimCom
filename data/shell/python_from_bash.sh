$ python -c "print 5.5*3"
16.5

$ num=`python -c "print 5.5*3"`
$ echo $num
16.5

# you can also try pythonpy ( http://redd.it/27ngm0 )
# sudo pip install pythonpy; alias py='pythonpy'
$ py '3 * 1.5'
4.5

$ py 'range(3)'
0
1
2

$ py 'random.random()'
0.103173957713

# -x: line by line
$ py 'range(3)' | py -x 'x + ".txt"'
0.txt
1.txt
2.txt

# -fx: filter line by line
$ py 'range(8)' | py -fx 'int(x)%2 == 1'
1
3
5
7
