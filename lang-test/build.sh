for f in loop conditional function array inline
do
    # COMPILE.
    ../lang $f.lng $f.asm
    cat $f.asm
    cp $f.asm ../asm
done

# ASSEMBLE.
cd ..
python3 asm.py $f.asm
cd -
