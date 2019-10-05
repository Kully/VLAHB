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
char namespace[64];

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

void Tag(int argc, char* argv[])
{
    int j = 0;
    for(int i = 0; i < sizeof(namespace); i++)
    {
        const char c = toupper(argv[2][i]);
        if(c == '\0')
            break;
        if(isalnum(c))
            namespace[j++] = c;
    }
}

void Open(int argc, char* argv[])
{
    Reset();
    Tag(argc, argv);
    fi = fopen(argv[1], "r");
    fo = fopen(argv[2], "w");
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
    fprintf(fo, "\tLD R[%d] %c\n", sp, tape);
    sp++;
}

void Load2(const int name)
{
    const int temp = idents[name];
    fprintf(fo, "\tLD R[%d] R[%d]\n", sp, temp);
    sp++;
}

void Mul(void)
{
    sp--;
    fprintf(fo, "\tMUL R[%d] R[%d]\n", sp - 1, sp);
}

void Div(void)
{
    sp--;
    fprintf(fo, "\tDIV R[%d] R[%d]\n", sp - 1, sp);
}

void Add(void)
{
    sp--;
    fprintf(fo, "\tADD R[%d] R[%d]\n", sp - 1, sp);
}

void Sub(void)
{
    sp--;
    fprintf(fo, "\tSUB R[%d] R[%d]\n", sp - 1, sp);
}

void Push(const int args)
{
    fprintf(fo, "\tPUSH\n");
    for(int i = 0; i < args; i++)
        fprintf(fo, "\tLD R[%d] R[%d]\n", i, i + sp);
}

void Pop(void)
{
    fprintf(fo, "\tPOP\n");
    fprintf(fo, "\tLD R[%d] R[4100]\n", sp);
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
    fprintf(fo, "\tCALL %c\n", name);
    Pop();
    sp++;
}

void Indirect(void)
{
    const int name = tape;
    Spin();
    if(tape == '=')
    {
        int temp = -1;
        if(idents[name] == -1)
            idents[name] = sp;
        else
        {
            temp = sp;
            sp = idents[name];
        }
        Match('=');
        Expression();
        if(temp != -1)
            sp = temp;
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
    fprintf(fo, "\tCMP R[%d] 0\n", sp - 1);
    fprintf(fo, "\tGOTO L%d\n", l0);
    fprintf(fo, "\tGOTO L%d\n", l1);
    fprintf(fo, "%s_L%d:\n", namespace, l0);
    Block();
    fprintf(fo, "%s_L%d:\n", namespace, l1);
}

void Return(void)
{
    fprintf(fo, "\tLD R[4100] R[%d]\n", CLAMP(sp - 1));
    fprintf(fo, "\tRET\n");
}

void Loop(void)
{
    const int l0 = label++;
    Match('@');
    fprintf(fo, "%s_L%d:\n", namespace, l0);
    Expression();
    fprintf(fo, "\tCMP R[%d] 0\n", sp - 1);
    Block();
    fprintf(fo, "\tGOTO L%d\n", l0);
}

void Expression(void)
{
    while(!End())
        if(tape == '?')
            Conditional();
        else if(tape == '@')
            Loop();
        else if(tape == '$')
        {
            Match('$');
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
        idents[tape] = sp;
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
    fprintf(fo, "%s_%c:\n", namespace, tape);
    Spin();
    Arguments();
    Block();
    Return();
    Copy(idents, temp);
}

int main(int argc, char* argv[])
{
    Open(argc, argv);
    while(tape != EOF)
        Function();
    Close();
}
