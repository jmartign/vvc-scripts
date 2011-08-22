import java.io.File;
import java.io.FileInputStream;
import java.math.BigInteger;
import com.ibm.spi.IBMCMSProvider;
import java.util.Date;
import java.util.Calendar;
import java.util.Enumeration;
import java.security.Security;
import java.security.KeyStore;
import java.security.cert.X509Certificate;

import org.w3c.dom.Document;
import org.w3c.dom.NamedNodeMap;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;

import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.DocumentBuilder;

class CertWatch {
	public static final String ROOT_ELEMENT = "keystores";
	public static final String STORE_ELEMENT = "keystore";

    public static void main(String[] args) {
    try {

        if (args.length < 1) {
            System.out.println("Usage: java CertWatch <argfile> ");
	    	return;
	}


        String ARGFILE = args[0];
        
        DocumentBuilderFactory docBuilderFactory = DocumentBuilderFactory.newInstance();
		docBuilderFactory.setIgnoringComments(true);
        DocumentBuilder docBuilder = docBuilderFactory.newDocumentBuilder();
        Document doc = docBuilder.parse (new File(ARGFILE));

		Node rootElement = doc.getFirstChild();
		if (rootElement.getNodeName().equalsIgnoreCase(ROOT_ELEMENT)){
			NodeList children = rootElement.getChildNodes();
			for (int i=0; i < children.getLength(); i++){
				Node child = (Node)children.item(i);
				if(child.getNodeName().equalsIgnoreCase(STORE_ELEMENT)){
					int	warning = 0;
					String location = null;
					String password = null;
					String dbtype = null;
					String sdays = null;
					int days = 30;
					NamedNodeMap attrs = child.getAttributes();
					if(attrs != null){
						Node item = attrs.getNamedItem("location");
						if(item==null) {
							throw new Exception("location attribute is mandatory");
						}
						location = item.getNodeValue();
						item = attrs.getNamedItem("password");
						if(item==null) {
							throw new Exception("password attribute is mandatory");
						}
						password = item.getNodeValue();
						item = attrs.getNamedItem("type");
						if(item==null) {
							dbtype="JKS";
						} else {
							dbtype = item.getNodeValue();
						}
						item = attrs.getNamedItem("nbrdays");
						if(item!=null){
						   sdays = item.getNodeValue();
        				   try {
        					if (sdays.length() > 1) {
            					days = Integer.parseInt(sdays);
							}
							}
							catch(NumberFormatException e) { 
								System.err.println("nbrdays in "+ARGFILE+" is in an invalid format.");
								return;
							}
						}
					}
					Calendar cal = Calendar.getInstance();
        			Date today = new Date();
					cal.setTime(today);
					cal.add(Calendar.DATE, days);
   	     			Date expiration = cal.getTime();
					if(!(new File(location)).exists()) {
						System.out.println("keystore file "+location+" not found!") ;
						System.exit(0) ;
					}
					try {
						Security.addProvider(new com.ibm.spi.IBMCMSProvider());
						KeyStore keystore = KeyStore.getInstance(dbtype);
						FileInputStream fis = new FileInputStream(location);
						keystore.load(fis, password.toCharArray());
						fis.close();
						Enumeration en = keystore.aliases();
						while (en.hasMoreElements()) {
							X509Certificate storecert = null;
							String ali = (String)en.nextElement() ;
							if(keystore.isCertificateEntry(ali) || keystore.isKeyEntry(ali) ) {
								storecert = (X509Certificate)keystore.getCertificate(ali);
								Date until = storecert.getNotAfter();
								if(until.before(expiration)) {
									if(warning == 0) {
										System.out.println("");
										System.out.println("The following certificates will expire within "+
														days+" days in keystore "+location);
										System.out.println("");
										warning=1;
									}
									System.out.println("Certificate "+ali+" expires on "+until);
								}
                                                        } else {
                                                          System.out.println("Unknown entry type found in the keystore: "+ali);
                                                        }
						}
					}
					catch (Exception e) {
   		         		System.err.println("Caught exception " + e.toString());
   		     		}
				}
			}
		} else {
			throw new Exception("Root element is incorrect");
		}
    }
	catch (Exception e) {
		System.err.println("Caught exception " + e.toString());
    }
    }
}
