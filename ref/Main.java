public class Main {
    public Integer t;

    public static void main(String[] args) {
        Integer i;
        Integer j = 2;
        String s = "1"; 
        s = null;
        i = 3;
        j = j + i;
        s = s + j + s;
        System.out.println(s);
        System.out.println(j);
        System.out.println(new Main().helper());
    }

    public int helper() {
        t = 2;
        return t;
    }
}