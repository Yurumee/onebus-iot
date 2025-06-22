import React, {useContext} from "react";
import { Text, View, Button } from "react-native";
import { AuthContext } from "../utils/authContext";

export default function Index() {
  const authContext = useContext(AuthContext);

  return (
    <View
      style={{
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Text>Edit app/index.tsx to edit this screen.</Text>
      {/* botão abaixo só pra demonstrar a função de deslogar */}
      <Button title="sair" onPress={authContext.logOut} />
    </View>
  );
}
