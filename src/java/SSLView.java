import java.net.*;
import java.io.*;
import javax.net.ssl.*;
import java.security.*;
import java.security.cert.*;

class SSLView {
public static void main(String[] args) throws Exception {
  String host;
  int port;

  if (args.length == 1) {
    String[] c = args[0].split(":");
    host = c[0];
    port = (c.length == 1) ? 443 : Integer.parseInt(c[1]);
  } else {
    System.out.println("Usage: java SSLView host[:port]");
    return;
  }

  SSLContext context = SSLContext.getInstance("TLS");
  TrustManagerFactory tmf =
	    TrustManagerFactory.getInstance(TrustManagerFactory.getDefaultAlgorithm());
  tmf.init((KeyStore)null);
  X509TrustManager defaultTrustManager = (X509TrustManager)tmf.getTrustManagers()[0];
  SavingTrustManager tm = new SavingTrustManager(defaultTrustManager);
  context.init(null, new TrustManager[] {tm}, null);
  SSLSocketFactory factory = context.getSocketFactory();

  System.out.println("Opening connection to " + host + ":" + port + "...");
  SSLSocket socket = (SSLSocket)factory.createSocket(host, port);
  try {
    System.out.println("Starting SSL handshake...");
    socket.startHandshake();
    socket.close();
    System.out.println("Trusted Certificate");
  } catch (SSLException e) {
    System.out.println("Invalid Certificate");
  }
  X509Certificate[] chain = tm.chain;
  if (chain == null) {
    System.out.println("Could not obtain server certificate chain");
    return;
  }
  BufferedReader reader =
		new BufferedReader(new InputStreamReader(System.in));

  System.out.println();
  System.out.println("Server sent " + chain.length + " certificate(s):");
  System.out.println();
  MessageDigest sha1 = MessageDigest.getInstance("SHA1");
  MessageDigest md5 = MessageDigest.getInstance("MD5");
  for (int i = 0; i < chain.length; i++) {
    X509Certificate cert = chain[i];
    System.out.println
    	(" " + (i + 1) + " Subject " + cert.getSubjectDN());
    System.out.println("   Issuer  " + cert.getIssuerDN());
    System.out.println("   From    " + cert.getNotBefore());
    System.out.println("   Until   " + cert.getNotAfter());
    sha1.update(cert.getEncoded());
    System.out.println("   sha1    " + toHexString(sha1.digest()));
    md5.update(cert.getEncoded());
    System.out.println("   md5     " + toHexString(md5.digest()));
    System.out.println();
  }
}
    private static final char[] HEXDIGITS = "0123456789abcdef".toCharArray();

    private static String toHexString(byte[] bytes) {
	StringBuilder sb = new StringBuilder(bytes.length * 3);
	for (int b : bytes) {
	    b &= 0xff;
	    sb.append(HEXDIGITS[b >> 4]);
	    sb.append(HEXDIGITS[b & 15]);
	    sb.append(' ');
	}
	return sb.toString();
    }

    private static class SavingTrustManager implements X509TrustManager {

	private final X509TrustManager tm;
	private X509Certificate[] chain;

	SavingTrustManager(X509TrustManager tm) {
	    this.tm = tm;
	}

	public X509Certificate[] getAcceptedIssuers() {
	    throw new UnsupportedOperationException();
	}

	public void checkClientTrusted(X509Certificate[] chain, String authType)
		throws CertificateException {
	    throw new UnsupportedOperationException();
	}

	public void checkServerTrusted(X509Certificate[] chain, String authType)
		throws CertificateException {
	    this.chain = chain;
	    tm.checkServerTrusted(chain, authType);
	}
    }

}
