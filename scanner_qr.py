import cv2
from pyzbar import pyzbar

def scan_qr_code():
    # Inicializa la cámara
    cap = cv2.VideoCapture(0)

    qr_data = None

    while True:
        # Lee un frame de la cámara
        ret, frame = cap.read()
        
        # Si no se puede leer el frame, sal del bucle
        if not ret:
            break

        # Detecta códigos QR en el frame
        decoded_objects = pyzbar.decode(frame)
        
        for obj in decoded_objects:
            qr_data = obj.data.decode('utf-8')
            # Dibuja un rectángulo alrededor del código QR
            (x, y, w, h) = obj.rect
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            # Muestra el dato decodificado
            cv2.putText(frame, qr_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Muestra el frame con el rectángulo
        cv2.imshow('QR Code Scanner', frame)
        
        # Si se presiona la tecla 'q', se sale del bucle
        if cv2.waitKey(1) & 0xFF == ord('q') or qr_data is not None:
            break

    # Libera la cámara y cierra todas las ventanas
    cap.release()
    cv2.destroyAllWindows()

    return qr_data

if __name__ == "__main__":
    qr_code_data = scan_qr_code()
    if qr_code_data:
        print(f"El dato del código QR es: {qr_code_data}")
    else:
        print("No se ha detectado ningún código QR.")
