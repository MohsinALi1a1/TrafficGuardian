# CREATE TABLE NakaGraph (
#     ID INT PRIMARY KEY AUTO_INCREMENT,
#     FromNakaID INT,
#     ToNakaID INT,
#     DistanceKM FLOAT,
#     FOREIGN KEY (FromNakaID) REFERENCES Naka(NakaID),
#     FOREIGN KEY (ToNakaID) REFERENCES Naka(NakaID)
# );

from Model.Configure import  db


# Naka Graph Model
class NakaGraph(db.Model):
    __tablename__ = 'NakaGraph'

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FromNakaID = db.Column(db.Integer, db.ForeignKey('Chowki.id'), nullable=False)
    ToNakaID = db.Column(db.Integer, db.ForeignKey('Chowki.id'), nullable=False)
    DistanceKM = db.Column(db.Float, nullable=False)

    # Relationship to Naka table for FromNaka and ToNaka

    # Corrected relationships
    from_naka = db.relationship(
        'Chowki',
        foreign_keys=[FromNakaID],
        back_populates='from_nakagraphs'
    )

    to_naka = db.relationship(
        'Chowki',
        foreign_keys=[ToNakaID],
        back_populates='to_nakagraphs'
    )



