import java.rmi.*;
import java.rmi.server.UnicastRemoteObject;

public class RegistryRMIServer
{
  public static void main(String[] argv)
  {
    System.setSecurityManager(new RMISecurityManager());
    try {
      RegistryRMIImplementation implementation = new RegistryRMIImplementation("RegistryRMIImplementationInstance");
    }
    catch (Exception e) {
      System.err.println("Exception occurred: " + e);
      System.exit(1);
    }
  }
}

