import java.net.*;
import java.io.*;
import javax.net.ssl.SSLException;

class SSLTest {
public static void main(String[] args) {
  try {
    if (args.length < 1) {
      System.out.println("Usage: java SSLTest url");
      return;
    }
    String u = args[0];
    URL url = new URL(u);
    URLConnection con = url.openConnection();
    con.getInputStream();
    System.out.println("Certificate valid");
  }
  catch (SSLException e) {
    System.out.println("Certificate invalid");
  }
  catch (Exception e) {
    System.err.println("Caught exception: " + e.toString());
  }
}
}
