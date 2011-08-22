import java.rmi.*;
import java.rmi.registry.*;
import java.rmi.server.*;

public class RegistryRMIClient
{
  public static void main(String[] argv)
  {
    System.setSecurityManager(new RMISecurityManager());
    if (argv.length != 5) {
      System.err.println("usage: java RegistryRMIClient RMI_Server_IP Domain Service Qualifier Message");
      System.exit(1);
    }
    String serverName = argv[0];
    String domain = argv[1];
    String service = argv[2];
    String qualifier = argv[3];
    String message = argv[4];

    try {
      RegistryRMIInterface RegistryServerObject = 
        (RegistryRMIInterface) Naming.lookup("rmi://"+serverName+"/RegistryRMIImplementationInstance");

      String reply = RegistryServerObject.getService(domain,service,qualifier, message);
        System.out.println("Server replied: " + reply);
    }
    catch(Exception e) {
      System.err.println("Exception occured: " + e);
      System.exit(1);
    }
    System.out.println("RMI connection successful");
 }
}
