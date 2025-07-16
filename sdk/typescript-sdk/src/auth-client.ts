import { createClient } from "@hey-api/client-fetch";

export const authclient = createClient({
  credentials: "include",
});
