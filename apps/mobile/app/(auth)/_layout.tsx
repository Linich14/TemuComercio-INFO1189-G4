import { Stack } from 'expo-router';

export default function Layout() {
    return (
        <Stack screenOptions={{ headerShown: false }}>
            <Stack.Screen name="index" options={{ title: 'Login' }} />
            <Stack.Screen name="Register" options={{ title: 'Register' }} />
            <Stack.Screen
                name="recoveryPassword"
                options={{ title: 'Recovery Password' }}
            />
        </Stack>
    );
}
