from app.extensions import db
from app.models.post import Post
from sqlalchemy import func, text
from datetime import datetime, timedelta


class PostService:

    # --- FEED HÍBRIDO (DISTÂNCIA + TEMPO) ---
    @staticmethod
    def get_hybrid_feed(lat, lng, page, limit):
        query = Post.query.filter_by(status="active")

        # Se tivermos localização, usamos a Fórmula de Haversine simplificada
        if lat is not None and lng is not None:
            # Cálculo de distância em KM (aproximado para SQL)
            # 6371 é o raio da Terra em KM
            haversine = text(
                "(6371 * acos(cos(radians(:lat)) * cos(radians(latitude)) * "
                "cos(radians(longitude) - radians(:lng)) + sin(radians(:lat)) * "
                "sin(radians(latitude))))"
            )

            # Ordenação Híbrida: Posts recentes E próximos ganham prioridade
            # Aqui você pode ajustar o "peso" da distância vs tempo
            return query.params(lat=lat, lng=lng) \
                .order_by(haversine.asc(), Post.created_at.desc()) \
                .paginate(page=page, per_page=limit)

        # Fallback: apenas por data se não houver GPS
        return query.order_by(Post.created_at.desc()).paginate(page=page, per_page=limit)

    # --- CRIAÇÃO ---
    @staticmethod
    def create_post(data, user_id):
        new_post = Post(
            pet_name=data.get('pet_name'),
            pet_type=data.get('pet_type'),
            category=data.get('category'),
            description=data.get('description'),
            date=data.get('date'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            user_id=user_id
        )
        db.session.add(new_post)
        db.session.commit()
        return new_post

    # --- BUSCA E SEGURANÇA ---
    @staticmethod
    def get_post_or_404(post_id):
        return Post.query.get_or_404(post_id)

    @staticmethod
    def get_posts_by_user(user_id):
        return Post.query.filter_by(user_id=user_id, status="active").all()

    @staticmethod
    def update_post_safe(post_id, user_id, data):
        # Trava de segurança: só encontra o post se o user_id bater
        post = Post.query.filter_by(id=post_id, user_id=user_id).first_or_404()

        for key, value in data.items():
            setattr(post, key, value)

        db.session.commit()
        return post

    # --- MAPA (PERFORMANCE) ---
    @staticmethod
    def get_all_active_pins():
        # .with_entities evita dar SELECT * e foca no que o mapa precisa
        pins = Post.query.filter_by(status="active").with_entities(
            Post.id, Post.latitude, Post.longitude, Post.category
        ).all()

        return [{"id": p.id, "lat": p.latitude, "lng": p.longitude, "category": p.category} for p in pins]

    # --- ADMIN ---
    @staticmethod
    def get_all_posts_admin(page, limit):
        # Admin vê TUDO, inclusive 'hidden' e 'inactive'
        return Post.query.paginate(page=page, per_page=limit)

    @staticmethod
    def update_post_admin(post_id, data):
        post = Post.query.get_or_404(post_id)
        for key, value in data.items():
            setattr(post, key, value)
        db.session.commit()
        return post