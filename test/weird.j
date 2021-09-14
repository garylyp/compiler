/*
 * Tests absolutely wacky and exotic <Atom> and <Exp>
 * rules. Most statements are parseable (i.e. Can produce a parse tree) 
 * but don't make semantic sense
 */
class Main {
    Void main() {
        Int member;
        Test test;

        member = 1;
        test = new Test();
        // <ATOM>
        // ====== SECTION 1a: <Assignment Based AtomStmt> ======
		this.member = 1-1;
        test.member = 2-3;
        new Test().member = 1-3;
        (1+1).member = 3 <= 3;
        null.member = 4-5;
        
        // ====== SECTION 1b: <ExpList Based AtomStmt> ======
        this(1+1);
        test(1+1);
        new Test()(1+1);
        (3<=2)(1+1, 2+3);
        null();

        // ====== SECTION 1c: <Basic Nested AtomStmt> ======
        this.test.member = 1+2;
        this.test.md();
        test().member = 2;
        new Test().member(3<3).test(2,2);

        // ====== SECTION 1d: <AtomStmt that makes no sense> ======
        null(1+1)(2+2,3+3);
        null.test(1,1)(3<3, !true, 2*3/4+2, "str") = id.member(2,3);
        ("1" + "2").member.test.member(1,2,3).test.member.id = this;

        // <EXP>
        // ====== SECTION 2a: <AExp only> ======
        println(1+1*2-1/2*4+(4-1*3));
        println(1+2*-2*-3/-4+2--3);

        // ====== SECTION 2b: <BExp only> ======
        println(!true||!false&&true||false||false&&true);
        println(!(true || (false && true || !false) && false) || false);

        // ====== SECTION 2c: <SExp only> ======
        println("test" + "member");
        println("test");
        
        // ====== SECTION 3: <Absolutely horrible expr + atom> ======
        null.test(1--2--3+2*3+(4/5),true || 1 * -2 < 4 / 5 && this.member(true, false).test || null && new Test())(3<3, !true, 2*3/4+2, "str") = id.member(2,3);
        ("1" + "2").member.test(1+this+null != new Test() * -2+(true || false && !this) || true) = this;
    }
}    

class Test {
    Int member;

    Void md() {
        println (1+1);
    }
}
