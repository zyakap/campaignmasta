package com.campaignmasta.data.local.dao;

import android.database.Cursor;
import android.os.CancellationSignal;
import androidx.annotation.NonNull;
import androidx.room.CoroutinesRoom;
import androidx.room.EntityInsertionAdapter;
import androidx.room.RoomDatabase;
import androidx.room.RoomSQLiteQuery;
import androidx.room.SharedSQLiteStatement;
import androidx.room.util.CursorUtil;
import androidx.room.util.DBUtil;
import androidx.sqlite.db.SupportSQLiteStatement;
import com.campaignmasta.data.local.entity.InfluencerEntity;
import java.lang.Class;
import java.lang.Exception;
import java.lang.Integer;
import java.lang.Object;
import java.lang.Override;
import java.lang.String;
import java.lang.SuppressWarnings;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.Callable;
import javax.annotation.processing.Generated;
import kotlin.Unit;
import kotlin.coroutines.Continuation;
import kotlinx.coroutines.flow.Flow;

@Generated("androidx.room.RoomProcessor")
@SuppressWarnings({"unchecked", "deprecation"})
public final class InfluencerDao_Impl implements InfluencerDao {
  private final RoomDatabase __db;

  private final EntityInsertionAdapter<InfluencerEntity> __insertionAdapterOfInfluencerEntity;

  private final SharedSQLiteStatement __preparedStmtOfDeleteAll;

  public InfluencerDao_Impl(@NonNull final RoomDatabase __db) {
    this.__db = __db;
    this.__insertionAdapterOfInfluencerEntity = new EntityInsertionAdapter<InfluencerEntity>(__db) {
      @Override
      @NonNull
      protected String createQuery() {
        return "INSERT OR REPLACE INTO `influencers` (`localId`,`serverId`,`fullName`,`phone`,`communityRole`,`influenceLevel`,`relationshipStatus`,`contactFrequencyDays`,`lastCallDate`,`nextContactDueDate`,`wardName`,`wardId`,`notes`,`updatedAt`) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)";
      }

      @Override
      protected void bind(@NonNull final SupportSQLiteStatement statement,
          @NonNull final InfluencerEntity entity) {
        statement.bindString(1, entity.getLocalId());
        statement.bindLong(2, entity.getServerId());
        statement.bindString(3, entity.getFullName());
        statement.bindString(4, entity.getPhone());
        statement.bindString(5, entity.getCommunityRole());
        statement.bindString(6, entity.getInfluenceLevel());
        statement.bindString(7, entity.getRelationshipStatus());
        statement.bindLong(8, entity.getContactFrequencyDays());
        if (entity.getLastCallDate() == null) {
          statement.bindNull(9);
        } else {
          statement.bindString(9, entity.getLastCallDate());
        }
        if (entity.getNextContactDueDate() == null) {
          statement.bindNull(10);
        } else {
          statement.bindString(10, entity.getNextContactDueDate());
        }
        statement.bindString(11, entity.getWardName());
        if (entity.getWardId() == null) {
          statement.bindNull(12);
        } else {
          statement.bindLong(12, entity.getWardId());
        }
        statement.bindString(13, entity.getNotes());
        statement.bindString(14, entity.getUpdatedAt());
      }
    };
    this.__preparedStmtOfDeleteAll = new SharedSQLiteStatement(__db) {
      @Override
      @NonNull
      public String createQuery() {
        final String _query = "DELETE FROM influencers";
        return _query;
      }
    };
  }

  @Override
  public Object insertAll(final List<InfluencerEntity> entities,
      final Continuation<? super Unit> $completion) {
    return CoroutinesRoom.execute(__db, true, new Callable<Unit>() {
      @Override
      @NonNull
      public Unit call() throws Exception {
        __db.beginTransaction();
        try {
          __insertionAdapterOfInfluencerEntity.insert(entities);
          __db.setTransactionSuccessful();
          return Unit.INSTANCE;
        } finally {
          __db.endTransaction();
        }
      }
    }, $completion);
  }

  @Override
  public Object deleteAll(final Continuation<? super Unit> $completion) {
    return CoroutinesRoom.execute(__db, true, new Callable<Unit>() {
      @Override
      @NonNull
      public Unit call() throws Exception {
        final SupportSQLiteStatement _stmt = __preparedStmtOfDeleteAll.acquire();
        try {
          __db.beginTransaction();
          try {
            _stmt.executeUpdateDelete();
            __db.setTransactionSuccessful();
            return Unit.INSTANCE;
          } finally {
            __db.endTransaction();
          }
        } finally {
          __preparedStmtOfDeleteAll.release(_stmt);
        }
      }
    }, $completion);
  }

  @Override
  public Flow<List<InfluencerEntity>> getAllFlow() {
    final String _sql = "SELECT * FROM influencers ORDER BY fullName ASC";
    final RoomSQLiteQuery _statement = RoomSQLiteQuery.acquire(_sql, 0);
    return CoroutinesRoom.createFlow(__db, false, new String[] {"influencers"}, new Callable<List<InfluencerEntity>>() {
      @Override
      @NonNull
      public List<InfluencerEntity> call() throws Exception {
        final Cursor _cursor = DBUtil.query(__db, _statement, false, null);
        try {
          final int _cursorIndexOfLocalId = CursorUtil.getColumnIndexOrThrow(_cursor, "localId");
          final int _cursorIndexOfServerId = CursorUtil.getColumnIndexOrThrow(_cursor, "serverId");
          final int _cursorIndexOfFullName = CursorUtil.getColumnIndexOrThrow(_cursor, "fullName");
          final int _cursorIndexOfPhone = CursorUtil.getColumnIndexOrThrow(_cursor, "phone");
          final int _cursorIndexOfCommunityRole = CursorUtil.getColumnIndexOrThrow(_cursor, "communityRole");
          final int _cursorIndexOfInfluenceLevel = CursorUtil.getColumnIndexOrThrow(_cursor, "influenceLevel");
          final int _cursorIndexOfRelationshipStatus = CursorUtil.getColumnIndexOrThrow(_cursor, "relationshipStatus");
          final int _cursorIndexOfContactFrequencyDays = CursorUtil.getColumnIndexOrThrow(_cursor, "contactFrequencyDays");
          final int _cursorIndexOfLastCallDate = CursorUtil.getColumnIndexOrThrow(_cursor, "lastCallDate");
          final int _cursorIndexOfNextContactDueDate = CursorUtil.getColumnIndexOrThrow(_cursor, "nextContactDueDate");
          final int _cursorIndexOfWardName = CursorUtil.getColumnIndexOrThrow(_cursor, "wardName");
          final int _cursorIndexOfWardId = CursorUtil.getColumnIndexOrThrow(_cursor, "wardId");
          final int _cursorIndexOfNotes = CursorUtil.getColumnIndexOrThrow(_cursor, "notes");
          final int _cursorIndexOfUpdatedAt = CursorUtil.getColumnIndexOrThrow(_cursor, "updatedAt");
          final List<InfluencerEntity> _result = new ArrayList<InfluencerEntity>(_cursor.getCount());
          while (_cursor.moveToNext()) {
            final InfluencerEntity _item;
            final String _tmpLocalId;
            _tmpLocalId = _cursor.getString(_cursorIndexOfLocalId);
            final int _tmpServerId;
            _tmpServerId = _cursor.getInt(_cursorIndexOfServerId);
            final String _tmpFullName;
            _tmpFullName = _cursor.getString(_cursorIndexOfFullName);
            final String _tmpPhone;
            _tmpPhone = _cursor.getString(_cursorIndexOfPhone);
            final String _tmpCommunityRole;
            _tmpCommunityRole = _cursor.getString(_cursorIndexOfCommunityRole);
            final String _tmpInfluenceLevel;
            _tmpInfluenceLevel = _cursor.getString(_cursorIndexOfInfluenceLevel);
            final String _tmpRelationshipStatus;
            _tmpRelationshipStatus = _cursor.getString(_cursorIndexOfRelationshipStatus);
            final int _tmpContactFrequencyDays;
            _tmpContactFrequencyDays = _cursor.getInt(_cursorIndexOfContactFrequencyDays);
            final String _tmpLastCallDate;
            if (_cursor.isNull(_cursorIndexOfLastCallDate)) {
              _tmpLastCallDate = null;
            } else {
              _tmpLastCallDate = _cursor.getString(_cursorIndexOfLastCallDate);
            }
            final String _tmpNextContactDueDate;
            if (_cursor.isNull(_cursorIndexOfNextContactDueDate)) {
              _tmpNextContactDueDate = null;
            } else {
              _tmpNextContactDueDate = _cursor.getString(_cursorIndexOfNextContactDueDate);
            }
            final String _tmpWardName;
            _tmpWardName = _cursor.getString(_cursorIndexOfWardName);
            final Integer _tmpWardId;
            if (_cursor.isNull(_cursorIndexOfWardId)) {
              _tmpWardId = null;
            } else {
              _tmpWardId = _cursor.getInt(_cursorIndexOfWardId);
            }
            final String _tmpNotes;
            _tmpNotes = _cursor.getString(_cursorIndexOfNotes);
            final String _tmpUpdatedAt;
            _tmpUpdatedAt = _cursor.getString(_cursorIndexOfUpdatedAt);
            _item = new InfluencerEntity(_tmpLocalId,_tmpServerId,_tmpFullName,_tmpPhone,_tmpCommunityRole,_tmpInfluenceLevel,_tmpRelationshipStatus,_tmpContactFrequencyDays,_tmpLastCallDate,_tmpNextContactDueDate,_tmpWardName,_tmpWardId,_tmpNotes,_tmpUpdatedAt);
            _result.add(_item);
          }
          return _result;
        } finally {
          _cursor.close();
        }
      }

      @Override
      protected void finalize() {
        _statement.release();
      }
    });
  }

  @Override
  public Flow<List<InfluencerEntity>> getDueFlow(final String today) {
    final String _sql = "SELECT * FROM influencers WHERE nextContactDueDate <= ? ORDER BY nextContactDueDate ASC";
    final RoomSQLiteQuery _statement = RoomSQLiteQuery.acquire(_sql, 1);
    int _argIndex = 1;
    _statement.bindString(_argIndex, today);
    return CoroutinesRoom.createFlow(__db, false, new String[] {"influencers"}, new Callable<List<InfluencerEntity>>() {
      @Override
      @NonNull
      public List<InfluencerEntity> call() throws Exception {
        final Cursor _cursor = DBUtil.query(__db, _statement, false, null);
        try {
          final int _cursorIndexOfLocalId = CursorUtil.getColumnIndexOrThrow(_cursor, "localId");
          final int _cursorIndexOfServerId = CursorUtil.getColumnIndexOrThrow(_cursor, "serverId");
          final int _cursorIndexOfFullName = CursorUtil.getColumnIndexOrThrow(_cursor, "fullName");
          final int _cursorIndexOfPhone = CursorUtil.getColumnIndexOrThrow(_cursor, "phone");
          final int _cursorIndexOfCommunityRole = CursorUtil.getColumnIndexOrThrow(_cursor, "communityRole");
          final int _cursorIndexOfInfluenceLevel = CursorUtil.getColumnIndexOrThrow(_cursor, "influenceLevel");
          final int _cursorIndexOfRelationshipStatus = CursorUtil.getColumnIndexOrThrow(_cursor, "relationshipStatus");
          final int _cursorIndexOfContactFrequencyDays = CursorUtil.getColumnIndexOrThrow(_cursor, "contactFrequencyDays");
          final int _cursorIndexOfLastCallDate = CursorUtil.getColumnIndexOrThrow(_cursor, "lastCallDate");
          final int _cursorIndexOfNextContactDueDate = CursorUtil.getColumnIndexOrThrow(_cursor, "nextContactDueDate");
          final int _cursorIndexOfWardName = CursorUtil.getColumnIndexOrThrow(_cursor, "wardName");
          final int _cursorIndexOfWardId = CursorUtil.getColumnIndexOrThrow(_cursor, "wardId");
          final int _cursorIndexOfNotes = CursorUtil.getColumnIndexOrThrow(_cursor, "notes");
          final int _cursorIndexOfUpdatedAt = CursorUtil.getColumnIndexOrThrow(_cursor, "updatedAt");
          final List<InfluencerEntity> _result = new ArrayList<InfluencerEntity>(_cursor.getCount());
          while (_cursor.moveToNext()) {
            final InfluencerEntity _item;
            final String _tmpLocalId;
            _tmpLocalId = _cursor.getString(_cursorIndexOfLocalId);
            final int _tmpServerId;
            _tmpServerId = _cursor.getInt(_cursorIndexOfServerId);
            final String _tmpFullName;
            _tmpFullName = _cursor.getString(_cursorIndexOfFullName);
            final String _tmpPhone;
            _tmpPhone = _cursor.getString(_cursorIndexOfPhone);
            final String _tmpCommunityRole;
            _tmpCommunityRole = _cursor.getString(_cursorIndexOfCommunityRole);
            final String _tmpInfluenceLevel;
            _tmpInfluenceLevel = _cursor.getString(_cursorIndexOfInfluenceLevel);
            final String _tmpRelationshipStatus;
            _tmpRelationshipStatus = _cursor.getString(_cursorIndexOfRelationshipStatus);
            final int _tmpContactFrequencyDays;
            _tmpContactFrequencyDays = _cursor.getInt(_cursorIndexOfContactFrequencyDays);
            final String _tmpLastCallDate;
            if (_cursor.isNull(_cursorIndexOfLastCallDate)) {
              _tmpLastCallDate = null;
            } else {
              _tmpLastCallDate = _cursor.getString(_cursorIndexOfLastCallDate);
            }
            final String _tmpNextContactDueDate;
            if (_cursor.isNull(_cursorIndexOfNextContactDueDate)) {
              _tmpNextContactDueDate = null;
            } else {
              _tmpNextContactDueDate = _cursor.getString(_cursorIndexOfNextContactDueDate);
            }
            final String _tmpWardName;
            _tmpWardName = _cursor.getString(_cursorIndexOfWardName);
            final Integer _tmpWardId;
            if (_cursor.isNull(_cursorIndexOfWardId)) {
              _tmpWardId = null;
            } else {
              _tmpWardId = _cursor.getInt(_cursorIndexOfWardId);
            }
            final String _tmpNotes;
            _tmpNotes = _cursor.getString(_cursorIndexOfNotes);
            final String _tmpUpdatedAt;
            _tmpUpdatedAt = _cursor.getString(_cursorIndexOfUpdatedAt);
            _item = new InfluencerEntity(_tmpLocalId,_tmpServerId,_tmpFullName,_tmpPhone,_tmpCommunityRole,_tmpInfluenceLevel,_tmpRelationshipStatus,_tmpContactFrequencyDays,_tmpLastCallDate,_tmpNextContactDueDate,_tmpWardName,_tmpWardId,_tmpNotes,_tmpUpdatedAt);
            _result.add(_item);
          }
          return _result;
        } finally {
          _cursor.close();
        }
      }

      @Override
      protected void finalize() {
        _statement.release();
      }
    });
  }

  @Override
  public Object countDue(final String today, final Continuation<? super Integer> $completion) {
    final String _sql = "SELECT COUNT(*) FROM influencers WHERE nextContactDueDate <= ?";
    final RoomSQLiteQuery _statement = RoomSQLiteQuery.acquire(_sql, 1);
    int _argIndex = 1;
    _statement.bindString(_argIndex, today);
    final CancellationSignal _cancellationSignal = DBUtil.createCancellationSignal();
    return CoroutinesRoom.execute(__db, false, _cancellationSignal, new Callable<Integer>() {
      @Override
      @NonNull
      public Integer call() throws Exception {
        final Cursor _cursor = DBUtil.query(__db, _statement, false, null);
        try {
          final Integer _result;
          if (_cursor.moveToFirst()) {
            final int _tmp;
            _tmp = _cursor.getInt(0);
            _result = _tmp;
          } else {
            _result = 0;
          }
          return _result;
        } finally {
          _cursor.close();
          _statement.release();
        }
      }
    }, $completion);
  }

  @NonNull
  public static List<Class<?>> getRequiredConverters() {
    return Collections.emptyList();
  }
}
