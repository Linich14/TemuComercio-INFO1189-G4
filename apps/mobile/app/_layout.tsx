import '../global.css';

import { Slot } from 'expo-router';
import { AuthProvider } from '~/src/providers/AuthProvider';
import { KeyboardProvider } from 'react-native-keyboard-controller';

export default function Root() {
    return (
        <AuthProvider>
            <KeyboardProvider>
                <Slot
                    screenOptions={{
                        headerShown: false,
                    }}
                />
            </KeyboardProvider>
        </AuthProvider>
    );
}
