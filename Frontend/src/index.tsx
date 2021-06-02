import React from "react";
import ReactDOM from "react-dom";
import { ApolloProvider } from "@apollo/react-hooks";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import * as serviceWorkerRegistration from "./serviceWorkerRegistration";
import reportWebVitals from "./reportWebVitals";
import { Client as Styletron } from "styletron-engine-atomic";
import { Provider as StyletronProvider } from "styletron-react";
import { BaseProvider, styled } from "baseui";
import { createTheme } from "baseui";

import "./index.css";
import App from "./App";
import ImagesAndUpload from "./pages/ImagesAndUpload";
import client from "./client";
const primitives = {
  primaryFontFamily: "Yeseva One",
};

const theme = createTheme(primitives);

const engine = new Styletron();

const Centered = styled("div", {
  height: "100%",
  paddingLeft: "30px",
  paddingRight: "30px",
  paddingTop: "30px",
});

ReactDOM.render(
  <React.StrictMode>
    <ApolloProvider client={client}>
      <StyletronProvider value={engine}>
        <BaseProvider theme={theme}>
          <Centered>
            <Router>
              <Switch>
                <Route path="/" exact>
                  <App />
                </Route>
                <Route path="/my-face" exact>
                  <ImagesAndUpload />
                </Route>
              </Switch>
            </Router>
          </Centered>
        </BaseProvider>
      </StyletronProvider>
    </ApolloProvider>
  </React.StrictMode>,
  document.getElementById("root")
);

serviceWorkerRegistration.register();

reportWebVitals();
