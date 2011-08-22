import java.rmi.*;
import java.rmi.server.UnicastRemoteObject;

public class RegistryRMIImplementation extends UnicastRemoteObject implements RegistryRMIInterface
{
  public RegistryRMIImplementation(String name) throws RemoteException
  {
    super();
    try {
      Naming.rebind(name, this);
    }
    catch(Exception e) {
      System.out.println("Exception occurred: " + e);
    }
  }
  public String getService(String Domain, String Service, String Qualifier, String Message)
  {
    return new String(Domain+":"+Service+":"+Qualifier+"("+Message+")");
  }
}
