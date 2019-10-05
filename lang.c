#include <stdio.h>
#include <ctype.h>
#include <assert.h>
#include <stdbool.h>

#define CLAMP(a) ((a) < 0 ? 0 : (a))

#define MAX 256

FILE* fi;
FILE* fo;

int tape;
int sp;
int idents[MAX];
int label;

void Expression(void);

void Block(void);

void Spin(void)
{
    tape = getc(fi);
    if(isspace(tape))
        Spin();
}

void Reset(void)
{
    for(int i = 0; i < MAX; i++)
        idents[i] = -1;
}

void Open(void)
{
    Reset();
    fi = fopen("a.lng", "r");
    fo = stdout;
    Spin();
}

void Close(void)
{
    fclose(fi);
    fclose(fo);
}

void Match(int c)
{
    assert(tape == c);
    Spin();
}

void Load1(void)
{
    fprintf(stdout, "\tLD R[%d] %c\n", sp, tape);
    sp++;
}

void Load2(const int name)
{
    const int temp = idents[name];
    fprintf(stdout, "\tLD R[%d] R[%d]\n", sp, temp);
    sp++;
}

void Mul(void)
{
    sp--;
    fprintf(stdout, "\tMUL R[%d] R[%d]\n", sp - 1, sp);
}

void Div(void)
{
    sp--;
    fprintf(stdout, "\tDIV R[%d] R[%d]\n", sp - 1, sp);
}

void Add(void)
{
    sp--;
    fprintf(stdout, "\tADD R[%d] R[%d]\n", sp - 1, sp);
}

void Sub(void)
{
    sp--;
    fprintf(stdout, "\tSUB R[%d] R[%d]\n", sp - 1, sp);
}

void Push(const int args)
{
    fprintf(stdout, "\tPUSH\n");
    for(int i = 0; i < args; i++)
        fprintf(stdout, "\tLD R[%d], R[%d]\n", i, i + sp);
}

void Pop(void)
{
    fprintf(stdout, "\tPOP\n");
    fprintf(stdout, "\tLD R[%d] R[4100]\n", sp);
}

void Call(const int name)
{
    Match('(');
    const int temp = sp;
    int args = 0;
    while(tape != ')')
    {
        Expression();
        args++;
        if(tape != ')')
            Match(',');
    }
    Match(')');
    sp = temp;
    Push(args);
    fprintf(stdout, "\tCALL %c\n", name);
    Pop();
    sp++;
}

void Indirect(void)
{
    const int name = tape;
    Spin();
    if(tape == '=')
    {
        assert(idents[name] == -1);
        idents[name] = sp; // First see if existing?
        Match('=');
        Expression();
    }
    else if(tape == '(')
        Call(name);
    else
        Load2(name);
}

void Direct(void)
{
    if(isdigit(tape))
        Load1();
    else if(tape == '+') Add();
    else if(tape == '-') Sub();
    else if(tape == '/') Div();
    else if(tape == '*') Mul();
    Spin();
}

int End(void)
{
    return tape == ';'
        || tape == ')'
        || tape == '{'
        || tape == ',';
}

void Conditional(void)
{
    const int l0 = label++;
    const int l1 = label++;
    Match('?');
    Expression();
    fprintf(stdout, "\tCMP R[%d] 0\n", sp - 1);
    fprintf(stdout, "\tGOTO L%d\n", l0);
    fprintf(stdout, "\tGOTO L%d\n", l1);
    fprintf(stdout, "L%d:\n", l0);
    Block();
    fprintf(stdout, "L%d:\n", l1);
}

void Return(void)
{
    fprintf(stdout, "\tLD R[4100] R[%d]\n", CLAMP(sp - 1));
    fprintf(stdout, "\tRET\n");
}

void Expression(void)
{
    while(!End())
        if(tape == '?')
            Conditional();
        else if(tape == '@')
        {
            Match('@');
            Expression();
            Return();
        }
        else isalpha(tape) ? Indirect() : Direct();
}

void Statement(void)
{
    Expression();
    Match(';');
}

void Arguments(void)
{
    Match('(');
    while(tape != ')')
    {
        Spin();
        sp++;
        if(tape != ')')
            Match(',');
    }
    Match(')');
}

void Block(void)
{
    Match('{');
    while(tape != '}')
        Statement();
    Match('}');
}

void Copy(int a[], int b[])
{
    for(int i = 0; i < MAX; i++)
        a[i] = b[i];
}

void Function(void)
{
    sp = 0;
    idents[tape] = 0;
    int temp[MAX];
    Copy(temp, idents);
    fprintf(stdout, "%c:\n", tape);
    Spin();
    Arguments();
    Block();
    Return();
    Copy(idents, temp);
}

int main(void)
{
    Open();
    while(tape != EOF)
        Function();
    Close();
}
