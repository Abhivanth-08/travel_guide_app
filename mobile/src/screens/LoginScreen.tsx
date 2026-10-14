import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet, Alert } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import client from '../api/client';

export default function LoginScreen({ navigation }: any) {
  const [email, setEmail] = useState('demo@example.com');
  const [password, setPassword] = useState('password123');

  const handleLogin = async () => {
    try {
      // In a real app we'd use a form data payload or adjust the backend for JSON login
      // We designed the backend to accept standard JSON for UserLogin.
      const response = await client.post('/auth/login', {
        email,
        password
      });
      await AsyncStorage.setItem('userToken', response.data.access_token);
      navigation.replace('Home');
    } catch (error) {
      Alert.alert("Login Failed", "Invalid credentials");
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Login</Text>
      <TextInput 
        style={styles.input} 
        placeholder="Email" 
        value={email}
        onChangeText={setEmail}
        autoCapitalize="none"
      />
      <TextInput 
        style={styles.input} 
        placeholder="Password" 
        value={password}
        onChangeText={setPassword}
        secureTextEntry
      />
      <Button title="Login" onPress={handleLogin} />
      <View style={{height: 10}} />
      <Button title="Register" onPress={() => navigation.navigate('Register')} type="clear" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', padding: 20 },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 20, textAlign: 'center' },
  input: { borderWidth: 1, borderColor: '#ccc', padding: 10, marginBottom: 15, borderRadius: 5 }
});
