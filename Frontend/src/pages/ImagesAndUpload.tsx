import * as React from "react";
import { useStyletron } from "baseui";
import gql from "graphql-tag";
import { Grid, Cell, ALIGNMENT } from "baseui/layout-grid";
import { StatefulTooltip } from "baseui/tooltip";
import { FileUploader } from "baseui/file-uploader";
import { Block } from "baseui/block";
import { useMutation, useQuery } from "@apollo/react-hooks";
import { Card, StyledAction, StyledBody } from "baseui/card";
import { Input } from "baseui/input";
import { Button } from "baseui/button";
import { ListItem, ListItemLabel } from "baseui/list";

const GET_IMAGES = gql`
  query {
    images {
      imageWithFaceBoundSrc
      imageSrc
      id
      name
      faces {
        id
        vertices

        id
        landmarks {
          id
        }
        detectionConfidence
        landmarkingConfidence
        joyLikelihood
      }
    }
  }
`;

const uploadImgMutation = gql`
  mutation UploadImag($file: String!, $name: String!) {
    uploadImage(file: $file, name: $name) {
      success
    }
  }
`;

const DELETE_IMAGE = gql`
  mutation DeleteImage($id: ID) {
    deleteImage(id: $id) {
      ok
    }
  }
`;
// https://overreacted.io/making-setinterval-declarative-with-react-hooks/
function useInterval(callback: any, delay: number | null) {
  const savedCallback = React.useRef(() => {});
  // Remember the latest callback.
  React.useEffect(() => {
    savedCallback.current = callback;
  }, [callback]);
  // Set up the interval.
  React.useEffect((): any => {
    function tick() {
      savedCallback.current();
    }
    if (delay !== null) {
      let id = setInterval(tick, delay);
      return () => clearInterval(id);
    }
  }, [delay]);
}

function useFakeProgress(): [number, () => void, () => void] {
  const [fakeProgress, setFakeProgress] = React.useState(0);
  const [isActive, setIsActive] = React.useState(false);
  function stopFakeProgress() {
    setIsActive(false);
    setFakeProgress(0);
  }
  function startFakeProgress() {
    setIsActive(true);
  }
  useInterval(
    () => {
      if (fakeProgress >= 100) {
        stopFakeProgress();
      } else {
        setFakeProgress(fakeProgress + 10);
      }
    },
    isActive ? 500 : null
  );
  return [fakeProgress, startFakeProgress, stopFakeProgress];
}

export default function Images() {
  const imageData = useQuery(GET_IMAGES);
  const [uploadImage] = useMutation(uploadImgMutation);

  const images = imageData?.data?.images as any[];

  const [progressAmount, startFakeProgress, stopFakeProgress] =
    useFakeProgress();

  return (
    <Outer>
      <Grid
        overrides={{
          Grid: {
            style: {
              height: "100%",
              width: "100%",
            },
          },
        }}
      >
        <Cell
          overrides={{
            Cell: {
              style: {
                height: "100%",
                width: "100%",
              },
            },
          }}
          span={[12, 2, 4]}
          align={ALIGNMENT.center}
        >
          <Block
            width="100%"
            height="100%"
            display="flex"
            justifyContent="center"
            alignItems="center"
          >
            <FileUploader
              onCancel={stopFakeProgress}
              onDrop={async (acceptedFiles, rejectedFiles) => {
                const toBase64 = (file: any) =>
                  new Promise((resolve, reject) => {
                    const reader = new FileReader();
                    reader.readAsDataURL(file);
                    reader.onload = () => resolve(reader.result);
                    reader.onerror = (error) => reject(error);
                  });

                const file = await toBase64(acceptedFiles[0]);
                console.log(file);

                uploadImage({
                  variables: {
                    file,
                    name: acceptedFiles[0].name,
                  },
                }).then(() => {
                  imageData?.refetch();
                });

                startFakeProgress();
              }}
              // progressAmount is a number from 0 - 100 which indicates the percent of file transfer completed
              progressAmount={progressAmount}
              progressMessage={
                progressAmount ? `Uploading... ${progressAmount}% of 100%` : ""
              }
            />
          </Block>
        </Cell>
        <Cell
          overrides={{
            Cell: {
              style: {
                height: "100%",
                width: "100%",
              },
            },
          }}
          align={ALIGNMENT.center}
        >
          {imageData.loading ? null : (
            <Grid
              overrides={{
                Grid: {
                  style: {
                    height: "100%",
                    width: "900px",
                  },
                },
              }}
            >
              {images?.map((image, index) => (
                <Cell span={[4]}>
                  <StatefulTooltip
                    content={() => (
                      <Block padding={"20px"}>
                        Hello, there! 👋
                        <Input placeholder="Focusable Element" />
                      </Block>
                    )}
                    returnFocus
                    autoFocus
                  >
                    <Card
                      overrides={{
                        Root: {
                          style: { width: "100%", marginBottom: "20px" },
                        },
                        HeaderImage: {
                          style: {
                            backgroundColor: "#000",
                            minHeight: "300px",
                            maxHeight: "300px",
                            width: "100%",
                          },
                        },
                      }}
                      headerImage={
                        image?.imageWithFaceBoundSrc || image.imageSrc
                      }
                      title=""
                    >
                      <StyledBody>
                        <ListItem
                          sublist
                          endEnhancer={() => (
                            <ListItemLabel>
                              {image?.faces?.length}
                            </ListItemLabel>
                          )}
                        >
                          <ListItemLabel>Face count</ListItemLabel>
                        </ListItem>
                      </StyledBody>
                      <StyledAction>
                        <Delete id={image.id} imageData={imageData} />
                      </StyledAction>
                    </Card>
                  </StatefulTooltip>
                </Cell>
              ))}
            </Grid>
          )}
        </Cell>
      </Grid>
    </Outer>
  );
}
const Outer: React.FunctionComponent<{}> = ({ children }) => {
  const [css] = useStyletron();
  return (
    <div
      className={css({
        height: "90vh",
        width: "95vw",
      })}
    >
      {children}
    </div>
  );
};

const Delete = ({ id, imageData }: any) => {
  const [deleteImage, { loading: deleteLoading }] = useMutation(DELETE_IMAGE);

  return (
    <Button
      overrides={{
        BaseButton: {
          style: { width: "100%", backgroundColor: "red" },
        },
      }}
      onClick={async () => {
        await deleteImage({
          variables: {
            id,
          },
        });

        imageData?.refetch();
      }}
      isLoading={deleteLoading}
    >
      Delete Image
    </Button>
  );
};
