public class Main {
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
    }
}