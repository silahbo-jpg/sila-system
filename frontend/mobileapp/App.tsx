import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import RegistroMunicipe from './screens/RegistroMunicipe';
import RegistroAmbulante from './screens/RegistroAmbulante';

const Stack = createNativeStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Municipe" component={RegistroMunicipe} />
        <Stack.Screen name="Ambulante" component={RegistroAmbulante} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

