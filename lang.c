// program
//    : statement+
//    ;
// statement
//    : 'if' paren_expr statement
//    | 'if' paren_expr statement 'else' statement
//    | 'while' paren_expr statement
//    | 'do' statement 'while' paren_expr ';'
//    | '{' statement* '}'
//    | expr ';'
//    | ';'
//    ;
// paren_expr
//    : '(' expr ')'
//    ;
// expr
//    : test
//    | id '=' expr
//    ;
// test
//    : sum
//    | sum '<' sum
//    ;
// sum
//    : term
//    | sum '+' term
//    | sum '-' term
//    ;
// term
//    : id
//    | integer
//    | paren_expr
//    ;
// id
//    : STRING
//    ;
// integer
//    : INT
//    ;
// STRING
//    : [a-z]+
//    ;
// INT
//    : [0-9]+
//    ;
// WS
//    : [ \r\n\t] -> skip

#include <stdio.h>
#include <ctype.h>
#include <assert.h>
#include <stdbool.h>

FILE* fi;
FILE* fo;

int tape;
int sp;

void Spin(void)
{
    tape = getc(fi);
    if(isspace(tape))
        Spin();
}

void Open(void)
{
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

void Load(void)
{
    fprintf(stdout, "\tLOAD R[%d] %c\n", sp, tape);
    sp++;
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

void Expression(void)
{
    while(tape != ';')
    {
        if(isdigit(tape))
            Load();
        else
        if(tape == '+')
            Add();
        else
        if(tape == '-')
            Sub();
        Spin();
    }
}

void Statement(void)
{
    Expression();
    Match(';');
}

void Function(void)
{
    sp = 0;
    const char name = tape;
    Spin();
    fprintf(stdout, "%c:\n", name);
    Match('(');
    Match(')');
    Match('{');
    while(tape != '}')
        Statement();
    Match('}');
    fprintf(stdout, "\tLD R[4100] R[%d]\n", sp - 1);
    fprintf(stdout, "\tRET\n");
}

int main(void)
{
    Open();
    while(tape != EOF)
        Function();
    Close();
}
