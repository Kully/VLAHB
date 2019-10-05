gcc ../lang.c

for f in loop conditional function
do
    echo "->$f:"
    ./a.out $f.lng $f.asm
    cat $f.asm
done
