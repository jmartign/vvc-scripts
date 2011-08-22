public interface RegistryRMIInterface extends java.rmi.Remote
{
  public String getService(String Domain, String Service, String Qualifier, String Message) throws java.rmi.RemoteException;
}
