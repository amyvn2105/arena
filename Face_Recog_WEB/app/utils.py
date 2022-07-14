from prepare import *

# Face recognition by image
def pipeline_model(path, filename):
    # %%time
    path_query = path
    orgimg = cv2.imread(path_query)  # BGR
    img = resize_image(orgimg.copy(), size_convert, orgimg)

    with torch.no_grad():
        pred = model(img[None, :])[0]

    # Apply NMS
    det = non_max_suppression_face(pred, conf_thres, iou_thres)[0]
    bboxs = np.int32(scale_coords(
        img.shape[1:], det[:, :4], orgimg.shape).round().cpu().numpy())

    for i in range(len(bboxs)):
        x1, y1, x2, y2 = bboxs[i]
        roi = orgimg[y1:y2, x1:x2]
        roi = face_preprocess(Image.fromarray(roi)).to(device)

        with torch.no_grad():
            emb_query = model_emb(roi[None, :]).cpu().numpy()
            emb_query = emb_query/np.linalg.norm(emb_query)

        scores = (emb_query @ emb_images.T)[0]

        id_min = np.argmax(scores)
        score = scores[id_min]
        name = name_images[id_min]

        if score < 0.3:
            caption = "UN_KNOWN"
            color = (0,0,255)
            cv2.rectangle(orgimg, (x1, y1), (x2, y2), color, 3)
            cv2.putText(orgimg, caption, (x1, y1-20), cv2.FONT_HERSHEY_PLAIN, 2, color, 2)
        else:
            caption = f"{name.split(' ')[0].upper()}:{score:.2f}"
            color = (0,255,0)
            cv2.rectangle(orgimg, (x1, y1), (x2, y2), color, 3)
            cv2.putText(orgimg, caption, (x1, y1-20), cv2.FONT_HERSHEY_PLAIN, 2, color, 2)

        """ t_size = cv2.getTextSize(caption, cv2.FONT_HERSHEY_PLAIN, 2, 2)[0]
        cv2.rectangle(orgimg, (x1, y1), (x2, y2), (0, 146, 230), 3)
        cv2.rectangle(
            orgimg, (x1, y1), (x1 + t_size[0], y1 + t_size[1]), (0, 146, 230), -1)
        cv2.putText(orgimg, caption, (x1, y1 +
                    t_size[1]), cv2.FONT_HERSHEY_PLAIN, 2, [255, 255, 255], 2) """
    cv2.imwrite('./static/predict/{}'.format(filename), orgimg)


def gen_frames():
    camera = cv2.VideoCapture(1)
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            img = resize_image(frame.copy(), size_convert, frame)
            with torch.no_grad():
                pred = model(img[None, :])[0]
            
            det = non_max_suppression_face(pred, conf_thres, iou_thres)[0]
            bboxs = np.int32(scale_coords(img.shape[1:], det[:, :4], frame.shape).round().cpu().numpy())

            if len(bboxs) <= 0:
                continue

            faces = torch.zeros((len(bboxs), 3, 112, 112), dtype=torch.float32)

            for i in range(len(bboxs)):
                x1, y1, x2, y2 = bboxs[i]
                roi = frame[y1:y2, x1:x2]
                faces[i] = face_preprocess(Image.fromarray(roi))

            with torch.no_grad():
                emb_query = model_emb(faces.to(device)).cpu().numpy()
                emb_query = emb_query/np.linalg.norm(emb_query)

            scores = (emb_query @ emb_images.T)
            idxs = np.argmax(scores, axis=-1)

            for i in range(len(bboxs)):
                x1, y1, x2, y2 = bboxs[i]

                score = scores[i, idxs[i]] 
                name = name_images[idxs[i]]
                if score <= 0.3:
                    caption = "UN_KNOWN"
                    color = (0,0,255)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3)
                    cv2.putText(frame, caption, (x1, y1-20), cv2.FONT_HERSHEY_PLAIN, 2, color, 2)
                else:
                    caption = f"{name.upper()}:{score:.2f}"
                    color = (0,255,0)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3)
                    cv2.putText(frame, caption, (x1, y1-20), cv2.FONT_HERSHEY_PLAIN, 2, color, 2)

            ret,buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')