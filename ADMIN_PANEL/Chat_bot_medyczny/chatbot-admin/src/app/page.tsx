import { auth0 } from "../lib/auth0";
import AuthButtons from "../components/AuthButtons";

export default async function HomePage() {
  const session = await auth0.getSession();

  return <AuthButtons session={session ?? null} />;
}
