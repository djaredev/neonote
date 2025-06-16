import { createClient } from "@hey-api/client-fetch";

export const authclient = createClient({
  baseUrl: "http://localhost:8000",
  credentials: "include",
});
