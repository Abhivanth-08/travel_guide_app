import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ActivityIndicator } from 'react-native';
import MapView, { Marker } from 'react-native-maps';
import client from '../api/client';
import AsyncStorage from '@react-native-async-storage/async-storage';
import * as Location from 'expo-location';

export default function MapScreen() {
  const [places, setPlaces] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [userLoc, setUserLoc] = useState({ lat: 11.0168, lng: 76.9558 }); // Coimbatore fallback
  const [isOffline, setIsOffline] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        let { status } = await Location.requestForegroundPermissionsAsync();
        let lat = 11.0168;
        let lng = 76.9558;
        
        if (status === 'granted') {
          let location = await Location.getCurrentPositionAsync({});
          lat = location.coords.latitude;
          lng = location.coords.longitude;
          setUserLoc({ lat, lng });
        }

        const response = await client.get(`/places/nearby?lat=${lat}&lng=${lng}&radius=50`);
        setPlaces(response.data);
        setIsOffline(false);
        // Cache places for offline
        await AsyncStorage.setItem('cached_places', JSON.stringify(response.data));
      } catch (error) {
        console.log("Network error, falling back to cache");
        setIsOffline(true);
        const cached = await AsyncStorage.getItem('cached_places');
        if (cached) {
          setPlaces(JSON.parse(cached));
        }
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color="#0000ff" />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {isOffline && (
        <View style={styles.offlineBanner}>
          <Text style={styles.offlineText}>Offline Mode - Showing Cached Data</Text>
        </View>
      )}
      <MapView 
        style={styles.map}
        initialRegion={{
          latitude: userLoc.lat,
          longitude: userLoc.lng,
          latitudeDelta: 0.0922,
          longitudeDelta: 0.0421,
        }}
      >
        <Marker 
          coordinate={{ latitude: userLoc.lat, longitude: userLoc.lng }}
          title="You are here"
          pinColor="blue"
        />
        {places.map((place) => (
          <Marker 
            key={place.id}
            coordinate={{ latitude: place.latitude, longitude: place.longitude }}
            title={place.name}
            description={place.category}
          />
        ))}
      </MapView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  map: { width: '100%', height: '100%' },
  center: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  offlineBanner: { backgroundColor: 'red', padding: 10, alignItems: 'center', zIndex: 1, position: 'absolute', top: 40, width: '100%' },
  offlineText: { color: 'white', fontWeight: 'bold' }
});
