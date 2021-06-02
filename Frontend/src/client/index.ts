import { ApolloClient } from "apollo-client";
import { setContext } from "apollo-link-context";
import { InMemoryCache } from "apollo-cache-inmemory";
import { ApolloLink } from "apollo-link";
import { HttpLink } from "apollo-link-http";

const delay = setContext(
  (request) =>
    new Promise((success, fail) => {
      setTimeout(() => {
        success("ok");
      }, 800);
    })
);

const cache = new InMemoryCache();
const http = new HttpLink({
  uri: "https://bareappapi.herokuapp.com/graphql",
});

const link = ApolloLink.from([delay, http]);

const client = new ApolloClient({
  link,
  cache,
});

export default client;
