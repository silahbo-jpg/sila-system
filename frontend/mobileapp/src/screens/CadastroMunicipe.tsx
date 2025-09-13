import React, { useState } from "react";
import { View, TextInput, Button, Text } from "react-native";

export default function CadastroMunicipe() {
  const [nome, setNome] = useState("");
  const [numeroBI, setNumeroBI] = useState("");

  const handleSubmit = () => {
    console.log({ nome, numeroBI });
    alert("(Mobile) Cadastro enviado: ver backend para integração real");
  };

  return (
    <View style={{ padding: 20 }}>
      <Text>Nome:</Text>
      <TextInput value={nome} onChangeText={setNome} style={{ borderWidth: 1, marginBottom: 10 }} />
      <Text>Nº BI:</Text>
      <TextInput value={numeroBI} onChangeText={setNumeroBI} style={{ borderWidth: 1, marginBottom: 10 }} />
      <Button title="Registrar Munícipe" onPress={handleSubmit} />
    </View>
  );
}

