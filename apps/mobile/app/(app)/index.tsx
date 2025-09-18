import { View, Text, Button } from 'react-native';
import { useAuth } from '../../src/features/auth/presentation/providers/AuthProvider';

export default function HomeScreen() {
    const { logout } = useAuth();

    const handleLogout = async () => {
        try {
            await logout(); // Llama a la función de logout
            console.log('Sesión cerrada correctamente');
        } catch (error) {
            console.error('Error al cerrar sesión:', error);
        }
    };

    return (
        <View className="flex-1 items-center justify-center">
            <Text>Pantalla Home</Text>
            <Button title="Cerrar sesión" onPress={handleLogout} />
        </View>
    );
}
