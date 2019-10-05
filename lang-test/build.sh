for f in loop conditional function
do
    ../lang $f.lng $f.asm
    cat $f.asm
done
