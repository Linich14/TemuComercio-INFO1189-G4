import '../global.css';

import { Stack } from 'expo-router';
import { AuthProvider } from '~/src/providers/AuthProvider';
import { KeyboardProvider } from 'react-native-keyboard-controller';

export default function Root() {
    return (
        <AuthProvider>
            <KeyboardProvider>
                <Stack
                    screenOptions={{
                        headerShown: false,
                    }}
                />
            </KeyboardProvider>
        </AuthProvider>
    );
}
