import React from "react";
import { FlexGrid, FlexGridItem } from "baseui/flex-grid";
import { Display2, Label3, Display1 } from "baseui/typography";
import { useStyletron } from "baseui";

import { Block, BlockProps } from "baseui/block";
import { useHistory } from "react-router";
import { styled } from "baseui";
import { darkGirlImage } from "./assets";
import { Button } from "baseui/button";

const itemProps: BlockProps = {
  // backgroundColor: "mono300",
  height: "98vh",
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
};

const Image = styled("img", {
  position: "absolute",
  top: "20%",
  left: "30%",
});

const App = () => {
  // eslint-disable-next-line
  const [css, theme] = useStyletron();
  const navigate = useHistory();

  return (
    <FlexGrid
      flexGridColumnCount={2}
      flexGridColumnGap="scale800"
      // flexGridRowGap="scale800"
      position="relative"
    >
      <FlexGridItem
        {...itemProps}
        alignItems="flex-start"
        paddingTop="scale1000"
        flexDirection="column"
      >
        <FlexGrid flexDirection="column">
          <Block>
            <Display2
              color={theme.colors.accent}
              marginBottom="scale500"
              width="80%"
              marginRight="scale800"
            >
              Glow your face & vitality with our best service
            </Display2>
            <Label3 paddingTop="20px">
              We provide beauty and treatment services with best quality, trust
              us
            </Label3>
          </Block>
        </FlexGrid>
        <Block marginTop="scale1000">
          <Button
            onClick={() => {
              navigate.push("my-face");
            }}
          >
            Let's get you started
          </Button>
        </Block>
      </FlexGridItem>
      <FlexGridItem
        {...itemProps}
        justifyContent="center"
        flexDirection="column"
      >
        <Display1 width="50%" color={theme.colors.accent} marginBottom="20px">
          "
        </Display1>
        <Label3 width="50%">
          Affordable, quality beauty treatement services for your skin, you'll
          come again
        </Label3>
      </FlexGridItem>
      <Image src={darkGirlImage} />
    </FlexGrid>
  );
};

export default App;
