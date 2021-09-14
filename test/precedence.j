/*
 * Tests operator precendence and disambiguation
 * of the operators.
 * Has boolean, arithmetic, string expressions, and 
 * method/member chaining operations
 */
class Main {
    Void main() {
        new Compare().test().square() = 1 + 1;
        this.test().member.member2(1+1).provider.provider2(1+1);
        t2 = compare.comparator.comp(1+1);
        t1 = 2;
        t3 = "\n\t\\\\ff\n\032\x08";
        t4=true||true&&false;
        t5=false&&true||true;
        t6=!(2<3&&3==2);
        t7="a"+"b"+"c";
        t8=1+2*-3;
        return 1 * 2 - 3 / 4 * 5;
    }
}